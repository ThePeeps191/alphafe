"""The policy/value network: a small encoder-decoder transformer.

* The encoder reads the tokenised proof state: each identity by itself first,
  then the identities together (``PolicyValueNet.encode``).
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

from .tokenizer import (BOS, EOS, MAX_MOVE_TOKENS, MAX_STATE_TOKENS, PAD, PIECE_STARTS, TOKEN_ID, VOCAB_SIZE,
                        MoveGrammar, sample_subterm_move, sample_uniform)


SRC_BUCKET = 64     # state token sequences are padded to a multiple of this
TGT_BUCKET = 8      # move token sequences likewise
MAX_SRC = MAX_STATE_TOKENS + 256     # longest state the network reads (a hindsight example adds its goal)
ROW_BUCKET = 8      # the number of pieces of a state is rounded up to a multiple of this


@dataclass
class ModelConfig:
    d_model: int = 192
    n_heads: int = 4
    enc_layers: int = 2         # layers that read one piece of the state (an identity) by itself
    row_layers: int = 2         # layers that read the pieces together, one vector for each
    row_width: int = 48         # tokens read together; a longer piece is read as several
    dec_layers: int = 2
    d_ff: int = 512
    dropout: float = 0.1
    vocab_size: int = VOCAB_SIZE
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
    """Encoder, decoder and value head.

    A state is a set of identities, up to 80 of them and often more than a
    thousand tokens. Reading it as one sequence costs the square of its
    length, which is why the network used to be shown the first 14
    identities only. The encoder here works in two steps instead. The state
    is laid out as a grid with one piece per row (the header, the original
    equation, each identity; a piece longer than ``row_width`` tokens takes
    several rows). ``enc_layers`` layers read every row by itself.
    ``row_layers`` layers then read one vector per row, the output at its
    first token, so every piece learns about the others. The output for a
    token is its own output plus the vector of its row. The cost grows with
    the number of tokens, and the decoder attends to all of them.
    """

    def __init__(self, config: ModelConfig = ModelConfig()):
        super().__init__()
        self.config = config
        d = config.d_model
        self.embed = nn.Embedding(config.vocab_size, d, padding_idx=PAD)
        self.src_pos = nn.Embedding(config.row_width, d)
        self.tgt_pos = nn.Embedding(config.max_tgt, d)

        def layer():
            return nn.TransformerEncoderLayer(d, config.n_heads, config.d_ff, config.dropout, batch_first=True, norm_first=True)

        dec_layer = nn.TransformerDecoderLayer(d, config.n_heads, config.d_ff, config.dropout, batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(layer(), config.enc_layers, enable_nested_tensor=False)
        self.row_encoder = nn.TransformerEncoder(layer(), config.row_layers, enable_nested_tensor=False)
        self.decoder = nn.TransformerDecoder(dec_layer, config.dec_layers)
        self.enc_norm = nn.LayerNorm(d)
        self.dec_norm = nn.LayerNorm(d)
        self.policy_head = nn.Linear(d, config.vocab_size)
        self.value_head = nn.Sequential(nn.Linear(d, d), nn.ReLU(), nn.Linear(d, 1))
        self.piece_start = torch.zeros(config.vocab_size, dtype=torch.bool)     # stays on the CPU, see ``layout``
        self.piece_start[[TOKEN_ID[token] for token in PIECE_STARTS]] = True

    def n_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def layout(self, src: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, int]:
        """Where each token of a batch of states sits in the grid: (row [B, S], column [B, S], number of rows).

        A row begins at every token that starts a piece and again after
        ``row_width`` tokens of one piece. Padding is sent to one spare row
        at the end. Worked out on the CPU, where the running sums it needs
        exist for integers on every backend.
        """
        width = self.config.row_width
        flat = src.cpu()
        index = torch.arange(flat.size(1)).expand_as(flat)
        starts = self.piece_start[flat]
        begun = torch.where(starts, index, torch.zeros_like(index)).cummax(dim=1).values     # where the token's piece began
        column = (index - begun) % width
        row = (starts | (column == 0)).long().cumsum(dim=1) - 1
        pad = flat == PAD
        rows = int(row.masked_fill(pad, 0).max()) + 2                  # one spare row for the padding
        rows = -(-rows // ROW_BUCKET) * ROW_BUCKET
        row = row.masked_fill(pad, rows - 1).clamp(min=0)
        column = column.masked_fill(pad, 0)
        return row.to(src.device), column.to(src.device), rows

    def encode(self, src: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """src: [B, S] token ids. Returns (memory [B, S, d], padding mask [B, S])."""
        pad = src == PAD
        batch, width, d = src.size(0), self.config.row_width, self.config.d_model
        row, column, rows = self.layout(src)
        which = torch.arange(batch, device=src.device).unsqueeze(1).expand_as(src)
        grid = torch.full((batch, rows, width), PAD, dtype=src.dtype, device=src.device)
        grid[which, row, column] = src                                  # padding writes padding into the spare row
        x = self.embed(grid) + self.src_pos(torch.arange(width, device=src.device))
        empty = grid == PAD
        blocked = empty.view(batch * rows, width).clone()
        blocked[:, 0] = False                                           # a row of padding only must still attend to something
        local = self.encoder(x.view(batch * rows, width, d), src_key_padding_mask=blocked).view(batch, rows, width, d)
        context = self.row_encoder(local[:, :, 0], src_key_padding_mask=empty[:, :, 0])
        memory = self.enc_norm(local[which, row, column] + context[which, row])
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


class StepDecoder:
    """Writes moves one token at a time without redoing the earlier positions.

    ``PolicyValueNet.decode`` runs the whole decoder over the partial move for
    every new token. The answer at a position depends only on the tokens up
    to it, so this class keeps, for each layer, the attention keys and values
    of the positions already written and computes only the new one. The
    encoder output is projected to cross-attention keys and values once.
    ``step`` returns the same logits as ``decode`` at that position, up to
    rounding (tests/test_model.py compares them).

    Every state gets ``k`` rows (the k samples drawn for it); row r of the
    token vector belongs to state r // k.
    """

    def __init__(self, model: PolicyValueNet, memory: torch.Tensor, pad: torch.Tensor, k: int, width: int = TGT_BUCKET):
        config = model.config
        self.model, self.k = model, k
        self.states, source_len, d = memory.shape
        self.heads, self.head_dim = config.n_heads, d // config.n_heads
        self.d = d
        for layer in model.decoder.layers:
            if not layer.norm_first or layer.activation is not F.relu or model.training:
                raise ValueError("StepDecoder supports the evaluation mode of a pre-norm ReLU decoder only")
        self.cross = []
        for layer in model.decoder.layers:
            weight, bias = layer.multihead_attn.in_proj_weight, layer.multihead_attn.in_proj_bias
            keys = self._heads(F.linear(memory, weight[d:2 * d], bias[d:2 * d])).unsqueeze(1)       # [B, 1, h, S, dh]
            values = self._heads(F.linear(memory, weight[2 * d:], bias[2 * d:])).unsqueeze(1)
            self.cross.append((keys.transpose(-2, -1), values))
        self.cross_block = pad.view(self.states, 1, 1, 1, source_len)                               # True: padding
        self.width = 0
        self.cache: list = [None] * len(model.decoder.layers)
        self._grow(width)

    def _heads(self, x: torch.Tensor) -> torch.Tensor:
        """[..., L, d] -> [..., h, L, dh]"""
        shape = x.shape[:-1] + (self.heads, self.head_dim)
        return x.view(shape).transpose(-3, -2)

    def _grow(self, width: int) -> None:
        """Make room for ``width`` positions (kept a multiple of TGT_BUCKET: MPS compiles a graph per shape)."""
        device = self.cross[0][1].device
        for index, old in enumerate(self.cache):
            shape = (self.states, self.k, self.heads, width, self.head_dim)
            keys, values = torch.zeros(shape, device=device), torch.zeros(shape, device=device)
            if old is not None:
                keys[:, :, :, : self.width] = old[0]
                values[:, :, :, : self.width] = old[1]
            self.cache[index] = (keys, values)
        self.width = width
        self.positions = torch.arange(width, device=device)

    def _attend(self, query: torch.Tensor, keys_t: torch.Tensor, values: torch.Tensor, block: torch.Tensor) -> torch.Tensor:
        """One query per row and head. query [B, k, h, 1, dh]; keys_t [..., dh, L]; values [..., L, dh]."""
        scores = (query @ keys_t) / (self.head_dim ** 0.5)
        weights = torch.softmax(scores.masked_fill(block, float("-inf")), dim=-1)
        return (weights @ values).reshape(self.states, self.k, self.d)

    @torch.no_grad()
    def step(self, tokens: torch.Tensor, position: int) -> torch.Tensor:
        """tokens: [B * k] ids written at ``position``. Returns the next-token logits [B * k, V]."""
        model, d = self.model, self.d
        if position >= self.width:
            self._grow(self.width + TGT_BUCKET)
        x = (model.embed(tokens) + model.tgt_pos(self.positions[position])).view(self.states, self.k, d)
        later = (self.positions > position).view(1, 1, 1, 1, self.width)                             # True: not written yet
        for layer, (keys, values), (cross_keys_t, cross_values) in zip(model.decoder.layers, self.cache, self.cross):
            attention = layer.self_attn
            q, key, value = F.linear(layer.norm1(x), attention.in_proj_weight, attention.in_proj_bias).split(d, dim=-1)
            shape = (self.states, self.k, self.heads, self.head_dim)
            keys[:, :, :, position] = key.view(shape)
            values[:, :, :, position] = value.view(shape)
            x = x + attention.out_proj(self._attend(q.view(shape).unsqueeze(-2), keys.transpose(-2, -1), values, later))
            attention = layer.multihead_attn
            q = F.linear(layer.norm2(x), attention.in_proj_weight[:d], attention.in_proj_bias[:d])
            x = x + attention.out_proj(self._attend(q.view(shape).unsqueeze(-2), cross_keys_t, cross_values, self.cross_block))
            x = x + layer.linear2(F.relu(layer.linear1(layer.norm3(x))))
        return model.policy_head(model.dec_norm(x)).view(self.states * self.k, -1)


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

# How many of the proposals for a state a search replaces by substitutions built from expressions
# already on the page (tokenizer.sample_subterm_move). A trained policy gives some whole kinds of
# move, x := f(x) for one, almost no probability, and no number of samples then finds them.
SUBTERM_PROPOSALS = 2


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
        # Round the batch up to a power of two with copies of the first state. MPS compiles a graph
        # per tensor shape, so there the batch is at least 16; on the CPU one state costs one state.
        size = 1 if torch.device(device).type == "cpu" else 16
        while size < n_real:
            size *= 2
        views = list(views) + [views[0]] * (size - n_real)
        src = pad_batch([v.tokens[:MAX_SRC] for v in views], device, SRC_BUCKET)
        memory, pad = self.model.encode(src)
        decoder = StepDecoder(self.model, memory, pad, k)
        grammars = [MoveGrammar(view) for view in views for _ in range(k)]
        batch = len(grammars)
        tokens = torch.full((batch,), BOS, dtype=torch.long, device=device)
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
            logits = decoder.step(tokens, position) + mask.to(device)
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
            tokens = torch.tensor(next_col, dtype=torch.long, device=device)
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


class VocabularyMismatch(ValueError):
    """A checkpoint was trained with a different token vocabulary than the code has now."""


def _code_version() -> str:
    """The git commit of the code, with "-dirty" if tracked files are modified; "" outside a checkout."""
    import pathlib
    import subprocess

    root = pathlib.Path(__file__).resolve().parent.parent

    def git(*args) -> str:
        try:
            done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            return ""
        return done.stdout.strip() if done.returncode == 0 else ""

    commit = git("rev-parse", "HEAD")
    if commit and git("status", "--porcelain", "--untracked-files=no"):
        commit += "-dirty"
    return commit


def save_checkpoint(path, model: PolicyValueNet, extra: dict) -> None:
    """Write a training checkpoint.

    Besides the weights it records the token vocabulary they were trained
    with (token ids mean nothing without it), the commit of the code and the
    torch version. All are plain strings, so ``weights_only`` loading works.
    """
    from .tokenizer import VOCAB

    torch.save({"config": asdict(model.config), "model": model.state_dict(), "vocab": list(VOCAB),
                "commit": _code_version(), "torch": str(torch.__version__), **extra}, path)


def check_vocabulary(payload: dict, path="") -> None:
    """Raise ``VocabularyMismatch`` unless the checkpoint's vocabulary is the current one.

    A checkpoint whose vocabulary differs still loads as tensors, and the
    grammar mask keeps its moves well formed, so nothing else would fail: the
    network would simply read and write the wrong symbols and score a little
    worse. Checkpoints written before the vocabulary was recorded (release
    v0.1.0) are accepted when the size matches.
    """
    from .tokenizer import VOCAB

    stored = payload.get("vocab")
    if stored is None:
        size = payload["config"].get("vocab_size")
        if size != len(VOCAB):
            raise VocabularyMismatch(
                f"checkpoint {path} was trained with {size} tokens and the code now has {len(VOCAB)}: "
                "retrain, or check out the version of the code the weights belong to")
        return
    if list(stored) != list(VOCAB):
        where = next((i for i, (a, b) in enumerate(zip(stored, VOCAB)) if a != b), min(len(stored), len(VOCAB)))
        theirs = stored[where] if where < len(stored) else "(nothing)"
        mine = VOCAB[where] if where < len(VOCAB) else "(nothing)"
        commit = payload.get("commit") or "an unrecorded commit"
        raise VocabularyMismatch(
            f"checkpoint {path} was trained with a different token vocabulary (token {where} is {theirs!r} there and "
            f"{mine!r} in the code now). It was trained at {commit}: retrain, or check out that version")


def load_model(path, device) -> tuple[PolicyValueNet, dict]:
    # weights_only=True: a checkpoint is tensors and plain values, never code,
    # so a file downloaded from someone else cannot run anything when loaded.
    payload = torch.load(path, map_location="cpu", weights_only=True)
    check_vocabulary(payload, path)
    model = PolicyValueNet(ModelConfig(**payload["config"]))
    model.load_state_dict(payload["model"])
    return model.to(device), payload


# What a published checkpoint keeps: the weights, how they were trained, and
# what they were trained with. The optimiser state and the random-number
# state (two thirds of a training checkpoint) are only needed to resume training.
EXPORT_KEYS = ("config", "model", "state", "train_config", "vocab", "commit", "torch")


def export_checkpoint(source, target) -> dict:
    """Write a weights-only copy of a training checkpoint, for sharing."""
    payload = torch.load(source, map_location="cpu", weights_only=True)
    slim = {key: payload[key] for key in EXPORT_KEYS if key in payload}
    slim["model"] = {name: tensor.detach().cpu().contiguous() for name, tensor in slim["model"].items()}
    torch.save(slim, target)
    return slim
