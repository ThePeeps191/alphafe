"""The policy/value network: a small encoder-decoder transformer.

* The encoder reads the tokenised proof state.
* The decoder writes the next move token by token (including the substitution
  term itself; there is no fixed pool of terms).
* A value head on the pooled encoder output estimates whether the state is solvable.

``NeuralProposer`` wraps the network for search: it samples moves under the
move grammar, so every sample is a well-formed move.
"""

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

warnings.filterwarnings("ignore", message="Failed to initialize NumPy")
warnings.filterwarnings("ignore", message="enable_nested_tensor")

import torch
import torch.nn as nn
import torch.nn.functional as F

from .tokenizer import (BOS, EOS, MAX_MOVE_TOKENS, MAX_STATE_TOKENS, PAD, VOCAB_SIZE, MoveGrammar,
                        sample_subterm_move, sample_uniform)


SRC_BUCKET = 64     # state token sequences are padded to a multiple of this
TGT_BUCKET = 8      # move token sequences likewise
MAX_SRC = 448       # longest state the network reads (longer ones are cut off)


@dataclass
class ModelConfig:
    d_model: int = 192
    n_heads: int = 4
    enc_layers: int = 4
    dec_layers: int = 2
    d_ff: int = 512
    dropout: float = 0.1
    vocab_size: int = VOCAB_SIZE
    max_src: int = MAX_SRC
    max_tgt: int = 56


def pick_device(prefer: str = "auto") -> torch.device:
    """CUDA if present, else Apple MPS, else CPU."""
    if prefer != "auto":
        return torch.device(prefer)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


class PolicyValueNet(nn.Module):
    def __init__(self, config: ModelConfig = ModelConfig()):
        super().__init__()
        self.config = config
        d = config.d_model
        self.embed = nn.Embedding(config.vocab_size, d, padding_idx=PAD)
        self.src_pos = nn.Embedding(config.max_src, d)
        self.tgt_pos = nn.Embedding(config.max_tgt, d)
        enc_layer = nn.TransformerEncoderLayer(d, config.n_heads, config.d_ff, config.dropout, batch_first=True, norm_first=True)
        dec_layer = nn.TransformerDecoderLayer(d, config.n_heads, config.d_ff, config.dropout, batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(enc_layer, config.enc_layers, enable_nested_tensor=False)
        self.decoder = nn.TransformerDecoder(dec_layer, config.dec_layers)
        self.enc_norm = nn.LayerNorm(d)
        self.dec_norm = nn.LayerNorm(d)
        self.policy_head = nn.Linear(d, config.vocab_size)
        self.value_head = nn.Sequential(nn.Linear(d, d), nn.ReLU(), nn.Linear(d, 1))

    def n_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def encode(self, src: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """src: [B, S] token ids. Returns (memory [B, S, d], padding mask [B, S])."""
        pad = src == PAD
        positions = torch.arange(src.size(1), device=src.device)
        x = self.embed(src) + self.src_pos(positions)
        memory = self.enc_norm(self.encoder(x, src_key_padding_mask=pad))
        return memory, pad

    def value(self, memory: torch.Tensor, pad: torch.Tensor) -> torch.Tensor:
        """Logit of "this state is solvable", from the mean of the encoder outputs."""
        keep = (~pad).unsqueeze(-1).to(memory.dtype)
        pooled = (memory * keep).sum(1) / keep.sum(1).clamp(min=1)
        return self.value_head(pooled).squeeze(-1)

    def decode(self, memory: torch.Tensor, pad: torch.Tensor, tgt_in: torch.Tensor) -> torch.Tensor:
        """tgt_in: [B, T] (starts with <bos>). Returns next-token logits [B, T, V]."""
        length = tgt_in.size(1)
        positions = torch.arange(length, device=tgt_in.device)
        y = self.embed(tgt_in) + self.tgt_pos(positions)
        causal = torch.triu(torch.ones(length, length, dtype=torch.bool, device=tgt_in.device), diagonal=1)
        out = self.decoder(y, memory, tgt_mask=causal, memory_key_padding_mask=pad, tgt_key_padding_mask=tgt_in == PAD)
        return self.policy_head(self.dec_norm(out))

    def forward(self, src: torch.Tensor, tgt_in: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        memory, pad = self.encode(src)
        return self.decode(memory, pad, tgt_in), self.value(memory, pad)


def pad_batch(sequences: list, device=None, multiple: int = 1) -> torch.Tensor:
    """Stack id lists into a padded tensor. ``multiple`` rounds the width up, which
    keeps the number of distinct tensor shapes small (Apple's MPS backend
    compiles and caches a graph per shape, so free-form shapes exhaust memory)."""
    width = max(len(s) for s in sequences)
    width = -(-width // multiple) * multiple
    out = torch.full((len(sequences), width), PAD, dtype=torch.long)
    for i, seq in enumerate(sequences):
        out[i, : len(seq)] = torch.tensor(seq, dtype=torch.long)
    return out.to(device) if device is not None else out


# Sampling temperatures for the proposals of one state. A trained policy is
# often almost certain of one move; sampling eight times at one temperature
# then returns the same move eight times. Spreading the temperatures keeps a
# few faithful samples and adds progressively more adventurous ones.
DIVERSE = (0.6, 0.8, 1.0, 1.0, 1.3, 1.6, 2.0, 3.0)


class NeuralProposer:
    """Samples moves from the network under the move grammar.

    ``temperature`` is one number, or a tuple that is cycled over the samples
    of each state (see ``DIVERSE``). Whatever temperature a sample was drawn
    at, the log-probability reported for it is the model's own (temperature
    1), so proposals from different temperatures can be ranked together.

    ``n_uniform`` of the ``k`` proposals per state are drawn from the uniform
    grammar policy instead (exploration during self-play; 0 for evaluation).
    """

    def __init__(self, model: PolicyValueNet, device, temperature=1.0, n_uniform: int = 0, rng=None,
                 max_batch: int = 2048, n_subterm: int = 0):
        self.model = model
        self.device = device
        self.n_subterm = n_subterm        # exploration proposals built from expressions in the state
        self.temperature = temperature
        self.n_uniform = n_uniform
        self.rng = rng
        self.max_batch = max_batch

    @torch.no_grad()
    def values(self, views: list) -> list:
        """Value-head probabilities for a list of states."""
        self.model.eval()
        out: list = []
        chunk = 256
        for begin in range(0, len(views), chunk):
            part = views[begin: begin + chunk]
            # Pad the batch to a power of two (MPS compiles a graph per shape).
            size = 16
            while size < len(part):
                size *= 2
            padded = list(part) + [part[0]] * (size - len(part))
            memory, pad = self.model.encode(pad_batch([v.tokens[:MAX_SRC] for v in padded], self.device, SRC_BUCKET))
            out.extend(torch.sigmoid(self.model.value(memory, pad)).tolist()[: len(part)])
        return out

    @torch.no_grad()
    def logprob(self, view, ids: list) -> float:
        """The model's log-probability of writing exactly this move in this state
        (under the grammar mask). Raises ValueError if the grammar cannot produce it."""
        self.model.eval()
        memory, pad = self.model.encode(pad_batch([view.tokens[:MAX_SRC]], self.device, SRC_BUCKET))
        grammar = MoveGrammar(view)
        tgt = [BOS]
        total = 0.0
        for token in ids:
            allowed = grammar.allowed()
            if token not in allowed:
                raise ValueError("the move grammar cannot produce this move")
            logits = self.model.decode(memory, pad, torch.tensor([tgt], device=self.device))[0, -1]
            mask = torch.full_like(logits, float("-inf"))
            mask[allowed] = 0.0
            total += F.log_softmax(logits + mask, dim=-1)[token].item()
            grammar.advance(token)
            tgt.append(token)
        return total

    @torch.no_grad()
    def propose(self, views: list, k: int) -> list:
        self.model.eval()
        k_net = max(k - self.n_uniform - self.n_subterm, 0)
        out: list = [dict() for _ in views]
        if k_net:
            chunk = max(1, self.max_batch // k_net)
            for begin in range(0, len(views), chunk):
                part = views[begin: begin + chunk]
                for offset, samples in enumerate(self._sample(part, k_net)):
                    bucket = out[begin + offset]
                    for ids, logp in samples:
                        key = tuple(ids)
                        if key not in bucket or logp > bucket[key]:
                            bucket[key] = logp
        if self.n_uniform or self.n_subterm:
            for view, bucket in zip(views, out):
                for _ in range(self.n_uniform):
                    ids, logp = sample_uniform(view, self.rng)
                    bucket.setdefault(tuple(ids), logp)
                for _ in range(self.n_subterm):
                    sample = sample_subterm_move(view, self.rng)
                    if sample is not None:
                        bucket.setdefault(tuple(sample[0]), sample[1])
        return [[(list(ids), logp) for ids, logp in bucket.items()] for bucket in out]

    def _sample(self, views: list, k: int) -> list:
        device = self.device
        n_real = len(views)
        # Round the batch up to a power of two (at least 16) with copies of the first state.
        size = 16
        while size < n_real:
            size *= 2
        views = list(views) + [views[0]] * (size - n_real)
        src = pad_batch([v.tokens[:MAX_SRC] for v in views], device, SRC_BUCKET)
        memory, pad = self.model.encode(src)
        memory = memory.repeat_interleave(k, dim=0)
        pad = pad.repeat_interleave(k, dim=0)
        grammars = [MoveGrammar(view) for view in views for _ in range(k)]
        batch = len(grammars)
        # The partial moves live in a fixed-width buffer (grown in steps of
        # TGT_BUCKET); position t of the decoder output only depends on tokens
        # up to t, so the padding to its right is harmless.
        tgt = torch.full((batch, TGT_BUCKET), PAD, dtype=torch.long, device=device)
        tgt[:, 0] = BOS
        ladder = self.temperature if isinstance(self.temperature, (tuple, list)) else (self.temperature,)
        temps = torch.tensor([ladder[j % len(ladder)] for _ in range(len(views)) for j in range(k)],
                             dtype=torch.float32, device=device).unsqueeze(1)
        logps = torch.zeros(batch, device=device)
        vocab = self.model.config.vocab_size
        for position in range(MAX_MOVE_TOKENS + 1):
            rows, cols = [], []
            for i, grammar in enumerate(grammars):
                if not grammar.done:
                    allowed = grammar.allowed()
                    rows.extend([i] * len(allowed))
                    cols.extend(allowed)
            if not rows:
                break
            mask = torch.full((batch, vocab), float("-inf"))
            mask[rows, cols] = 0.0
            active = torch.tensor([not g.done for g in grammars], device=device)
            logits = self.model.decode(memory, pad, tgt)[:, position, :] + mask.to(device)
            logits[~active] = 0.0                      # finished rows: any distribution, result ignored
            log_probs = F.log_softmax(logits, dim=-1)  # the model's own probabilities (for ranking)
            choice = torch.multinomial(F.softmax(logits / temps, dim=-1), 1).squeeze(1)
            logps = logps + torch.where(active, log_probs.gather(1, choice.unsqueeze(1)).squeeze(1), torch.zeros_like(logps))
            choice_list = choice.tolist()
            next_col = []
            for i, grammar in enumerate(grammars):
                if grammar.done:
                    next_col.append(PAD)
                else:
                    grammar.advance(choice_list[i])
                    next_col.append(choice_list[i])
            if position + 1 >= tgt.size(1):
                extra = torch.full((batch, TGT_BUCKET), PAD, dtype=torch.long, device=device)
                tgt = torch.cat([tgt, extra], dim=1)
            tgt[:, position + 1] = torch.tensor(next_col, dtype=torch.long, device=device)
        logp_list = logps.tolist()
        out = []
        for v in range(n_real):
            samples = []
            for j in range(k):
                grammar = grammars[v * k + j]
                if grammar.done:
                    samples.append((grammar.ids, logp_list[v * k + j]))
            out.append(samples)
        return out


def save_checkpoint(path, model: PolicyValueNet, extra: dict) -> None:
    torch.save({"config": asdict(model.config), "model": model.state_dict(), **extra}, path)


def load_model(path, device) -> tuple[PolicyValueNet, dict]:
    # weights_only=True: a checkpoint is tensors and plain values, never code,
    # so a file downloaded from someone else cannot run anything when loaded.
    payload = torch.load(path, map_location="cpu", weights_only=True)
    model = PolicyValueNet(ModelConfig(**payload["config"]))
    model.load_state_dict(payload["model"])
    return model.to(device), payload


# What a published checkpoint keeps: the weights and how they were trained.
# The optimiser state and the random-number state (two thirds of a training
# checkpoint) are only needed to resume training.
EXPORT_KEYS = ("config", "model", "state", "train_config")


def export_checkpoint(source, target) -> dict:
    """Write a weights-only copy of a training checkpoint, for sharing."""
    payload = torch.load(source, map_location="cpu", weights_only=True)
    slim = {key: payload[key] for key in EXPORT_KEYS if key in payload}
    slim["model"] = {name: tensor.detach().cpu().contiguous() for name, tensor in slim["model"].items()}
    torch.save(slim, target)
    return slim
