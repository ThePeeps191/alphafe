"""Self-play training: the network learns from its own proof attempts.

Each iteration:

1. sample synthetic training problems from the current curriculum tiers;
2. search for proofs with the current network (plus some uniform-random
   proposals for exploration); every proof is checked by the exact checker;
3. turn the attempts into training examples:
   * *solve* examples: on a successful proof, (state -> the move that was played);
   * *hindsight* examples: any accepted move, successful attempt or not,
     derived some new identity G; (state, goal G -> that move) is a correct
     example of how to derive G;
   * *value* examples: states on successful proofs are labelled solvable,
     states of failed attempts unsolvable;
4. take gradient steps on a replay buffer of such examples;
5. raise the tier when the solve rate on the current tier is high enough.

Nothing here uses the brute-force baseline, the seed benchmark, the real
benchmark, or the held-out synthetic test split.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import time
from dataclasses import asdict, dataclass, field

import torch
import torch.nn.functional as F

from .generate import N_TIERS, benchmark_keys, generate, protected_keys
from .model import (DIVERSE, SRC_BUCKET, TGT_BUCKET, ModelConfig, NeuralProposer, PolicyValueNet, check_vocabulary,
                    pad_batch, pick_device, save_checkpoint)
from .search import BestFirstSearch, GreedySearch, UniformProposer, run_searches
from . import terms as T
from .algebra import Poly
from .checker import Problem, Reject
from .env import start, step
from .moves import Onto, Split, Subst
from .tokenizer import BOS, PAD, decode_move, encode_move, encode_state

ROOT = pathlib.Path(__file__).resolve().parent.parent


@dataclass
class TrainConfig:
    run: str = "default"
    seed: int = 0
    per_tier: int = 3000            # synthetic problems generated per tier (about 10% are held out)
    start_tier: int = 1
    max_tier: int = N_TIERS
    iterations: int = 1000
    minutes: float = 28.0           # wall-clock limit for one run
    problems_per_iter: int = 192
    budget: int = 48                # checker calls per self-play attempt
    k: int = 8                      # proposals per expanded state ...
    n_uniform: int = 2              # ... of which this many are uniform-random (exploration)
    n_subterm: int = 0              # ... and this many substitute an expression already in the state
    temperature: float = 1.0
    diverse: bool = True            # sample proposals at a spread of temperatures (model.DIVERSE)
    steps_per_iter: int = 60
    batch_size: int = 128
    lr: float = 3e-4
    warmup: int = 200
    weight_decay: float = 0.01
    value_weight: float = 0.5
    minimise: bool = True              # drop unneeded moves from found proofs before learning from them
    mirror: bool = True                # also learn each proof with the names x and y exchanged
    hindsight_fraction: float = 0.25   # share of each batch
    negative_fraction: float = 0.15
    buffer_size: int = 120_000
    promote_at: float = 0.75           # self-play solve rate on the current tier needed to move up
    min_iters_per_tier: int = 6
    max_iters_per_tier: int = 25
    eval_every: int = 10
    eval_problems: int = 100
    eval_budget: int = 32
    device: str = "auto"
    model: dict = field(default_factory=lambda: asdict(ModelConfig()))


class ProblemPool:
    """Synthetic problems by tier, split into train and held-out test by canonical hash.

    ``for_training`` builds the pool a training run uses. It differs from
    the plain pool (the one the frozen held-out file was cut from) in two
    ways. No problem in it is a benchmark problem or a twin of one
    (``generate.protected_keys``): the hash split alone lets a held-out
    problem's sign-flipped twin into the training half. And problems that
    the environment solves by itself are left out, because a search on them
    never proposes a move and so teaches nothing.
    """

    def __init__(self, seed: int, per_tier: int, for_training: bool = False):
        data = generate(seed, per_tier, exclude=protected_keys() if for_training else benchmark_keys())
        if for_training:
            data = {tier: [g for g in items if not _solved_at_start(g)] for tier, items in data.items()}
        self.train = {tier: [g for g in items if g.split == "train"] for tier, items in data.items()}
        self.test = {tier: [g for g in items if g.split == "test"] for tier, items in data.items()}

    def sample_train(self, rng: random.Random, tier: int, n: int) -> list:
        """Half from the current tier, half spread over the earlier ones."""
        out = []
        for _ in range(n):
            pick = tier if tier == 1 or rng.random() < 0.5 else rng.randint(1, tier - 1)
            out.append(rng.choice(self.train[pick]))
        return out


def _solved_at_start(item) -> bool:
    try:
        state, _ = start(item.problem())
    except Reject:
        return True
    return state.solved


class ReplayBuffer:
    """Three bounded lists of examples: solve, hindsight and negative-value."""

    def __init__(self, size: int):
        self.size = size
        self.solve: list = []       # (src ids, move ids)   value target 1
        self.hindsight: list = []   # (src ids with goal, move ids)
        self.negative: list = []    # (src ids,)            value target 0

    def add(self, kind: str, item: tuple) -> None:
        store = getattr(self, kind)
        store.append(item)
        limit = self.size if kind != "negative" else self.size // 4
        if len(store) > limit:
            del store[: len(store) - limit]

    def __len__(self) -> int:
        return len(self.solve) + len(self.hindsight) + len(self.negative)


_SWAP_NAME = {"x": "y", "y": "x"}


def _swap_term(term: T.Term) -> T.Term:
    """Rename x <-> y in a term."""
    if isinstance(term, T.Var):
        return T.Var(_SWAP_NAME.get(term.name, term.name))
    if isinstance(term, (T.Add, T.Sub, T.Mul)):
        return type(term)(_swap_term(term.left), _swap_term(term.right))
    if isinstance(term, (T.Neg, T.App)):
        return type(term)(_swap_term(term.arg))
    if isinstance(term, T.Pow):
        return T.Pow(_swap_term(term.base), term.exp)
    return term


def swapped_examples(problem: Problem, moves: list) -> list:
    """The same proof for the same problem with the names x and y exchanged.

    Exchanging the two variable names turns a problem into an equally valid
    one, and a proof into a proof. Training on both stops the network from
    learning habits such as "always substitute for y". The mirrored proof is
    replayed through the checker, so the examples are real (state, move)
    pairs; if anything fails to carry over, no examples are returned.
    """
    if set(problem.poly.variables()) != {"x", "y"}:
        return []
    swap = {"x": Poly.var("y"), "y": Poly.var("x")}
    mirror = Problem(problem.equation + "  [x <-> y]", problem.domain, problem.poly.subst(swap), problem.name)
    state, _ = start(problem)
    mirrored, _ = start(mirror)
    pairs = []
    try:
        for move in moves:
            if state.solved or mirrored.solved:
                return []

            def row(index):
                wanted = state.current.rows[index].subst(swap)
                return mirrored.current.rows.index(wanted)      # ValueError if absent

            if isinstance(move, Subst):
                target = "P" if move.target == "P" else row(move.target)
                new = Subst(target, tuple((_SWAP_NAME.get(n, n), _swap_term(t)) for n, t in move.bindings))
            elif isinstance(move, Split):
                new = Split(row(move.target))
            elif isinstance(move, Onto):
                new = Onto(row(move.target), _SWAP_NAME.get(move.var, move.var))
            else:
                new = move                                      # SplitNZ, Pre: no variables involved
            view = encode_state(mirrored)
            ids = encode_move(new, view)
            if ids is None:
                return []
            pairs.append((tuple(view.tokens), tuple(ids)))
            state, _ = step(state, move)
            mirrored, _ = step(mirrored, new)
    except (Reject, ValueError, IndexError):
        return []
    return pairs if mirrored.solved else []


def minimal_moves(search) -> list:
    """The creative moves of a successful search with useless ones removed (see ``minimal_examples``)."""
    path = search.solution_path()
    moves = [decode_move(node.move_ids, node.parent.view) for node in path[1:]]

    def solves(sequence):
        state, _ = start(search.problem)
        try:
            for move in sequence:
                if state.solved:
                    return False
                state, _ = step(state, move)
        except Reject:
            return False
        return state.solved

    index = 0
    while index < len(moves) and len(moves) > 1:
        shorter = moves[:index] + moves[index + 1:]
        if solves(shorter):
            moves = shorter
        else:
            index += 1
    return moves


def minimal_examples(search) -> list:
    """Solve examples from a successful search, with useless moves removed.

    A found proof can contain creative moves that were not needed. We try
    dropping each one and replaying the rest; if the problem is still solved
    the move was dead weight and teaching it would teach noise. The examples
    are rebuilt from the replay, so each (state, move) pair is consistent.
    Returns [(state tokens, move tokens), ...].
    """
    path = search.solution_path()
    moves = [decode_move(node.move_ids, node.parent.view) for node in path[1:]]

    def replay(sequence):
        state, _ = start(search.problem)
        pairs = []
        for move in sequence:
            if state.solved:
                return None  # leftover moves after the end: not a clean proof
            view = encode_state(state)
            ids = encode_move(move, view)
            if ids is None:
                return None
            try:
                state, _ = step(state, move)
            except Reject:
                return None
            pairs.append((tuple(view.tokens), tuple(ids)))
        return pairs if state.solved else None

    index = 0
    while index < len(moves) and len(moves) > 1:
        shorter = moves[:index] + moves[index + 1:]
        if replay(shorter) is not None:
            moves = shorter
        else:
            index += 1
    pairs = replay(moves)
    if pairs is None:  # should not happen; fall back to the path as found
        pairs = [(tuple(node.parent.view.tokens), tuple(node.move_ids)) for node in path[1:]]
    return pairs


def harvest(searches: list, buffer: ReplayBuffer, rng: random.Random, max_hindsight: int = 4,
            minimise: bool = True, mirror: bool = False) -> None:
    """Turn finished self-play searches into training examples."""
    for search in searches:
        path = search.solution_path()
        if len(path) > 1:
            if minimise:
                pairs = minimal_examples(search)
            else:
                pairs = [(tuple(node.parent.view.tokens), tuple(node.move_ids)) for node in path[1:]]
            if mirror:
                pairs = pairs + swapped_examples(search.problem, minimal_moves(search))
            for pair in pairs:
                buffer.add("solve", pair)
        if not path and search.root is not None:      # None: the checker could not load the equation
            picks = [search.root] + rng.sample(search.nodes, min(2, len(search.nodes)))
            for node in picks:
                if node.state.branches:
                    buffer.add("negative", (tuple(node.view.tokens),))
        derived = [n for n in search.nodes if n.parent is not None and n.fresh and n.parent.state.branches]
        for node in rng.sample(derived, min(max_hindsight, len(derived))):
            goal = rng.choice(node.fresh)
            view = encode_state(node.parent.state, goal=goal)
            if len(view.tokens) <= 440:
                buffer.add("hindsight", (tuple(view.tokens), tuple(node.move_ids)))


MAX_TRAIN_SRC = 360      # tokenizer.MAX_STATE_TOKENS: with routine substitutions applied, states are long
LENGTH_GROUPS = 3        # a batch is processed in this many length-sorted pieces


def make_batch(buffer: ReplayBuffer, config: TrainConfig, rng: random.Random, device) -> list:
    """Sample a mixed batch and return it as a few length-sorted pieces.

    Each piece is (src, tgt_in, tgt_out, value_target, value_mask). Sorting by
    state length before padding matters for speed: most states are short, and
    padding a whole batch to its longest member would waste most of the work.
    """
    n = config.batch_size
    n_hind = int(n * config.hindsight_fraction) if buffer.hindsight else 0
    n_neg = int(n * config.negative_fraction) if buffer.negative else 0
    n_solve = n - n_hind - n_neg if buffer.solve else 0

    def draw(store, count):
        out = []
        while len(out) < count:
            item = rng.choice(store)
            if len(item[0]) <= MAX_TRAIN_SRC or rng.random() < 0.02:
                out.append(item)
        return out

    rows = []    # (src, tgt, value target, value mask)
    rows += [(src[:MAX_TRAIN_SRC], tgt, 1.0, 1.0) for src, tgt in draw(buffer.solve, n_solve)]
    rows += [(src[:MAX_TRAIN_SRC], tgt, 0.0, 0.0) for src, tgt in draw(buffer.hindsight, n_hind)]
    rows += [(src[:MAX_TRAIN_SRC], (), 0.0, 1.0) for (src,) in draw(buffer.negative, n_neg)]
    rows.sort(key=lambda row: len(row[0]))
    pieces = []
    size = -(-len(rows) // LENGTH_GROUPS)
    for begin in range(0, len(rows), size):
        part = rows[begin: begin + size]
        src = pad_batch([list(r[0]) for r in part], device, SRC_BUCKET)
        tgt_in = pad_batch([[BOS] + list(r[1])[:-1] if r[1] else [BOS] for r in part], device, TGT_BUCKET)
        tgt_out = pad_batch([list(r[1]) if r[1] else [PAD] for r in part], device, TGT_BUCKET)
        values = torch.tensor([r[2] for r in part], device=device)
        masks = torch.tensor([r[3] for r in part], device=device)
        pieces.append((src, tgt_in, tgt_out, values, masks))
    return pieces


def train_steps(model, optimizer, buffer: ReplayBuffer, config: TrainConfig, rng, device, step: int) -> tuple[dict, int]:
    model.train()
    totals = {"policy_loss": 0.0, "value_loss": 0.0}
    for _ in range(config.steps_per_iter):
        step += 1
        lr = config.lr * min(1.0, step / config.warmup)
        for group in optimizer.param_groups:
            group["lr"] = lr
        pieces = make_batch(buffer, config, rng, device)
        n_tokens = sum(int((p[2] != PAD).sum()) for p in pieces)
        n_values = sum(float(p[4].sum()) for p in pieces)
        optimizer.zero_grad()
        for src, tgt_in, tgt_out, value_target, value_mask in pieces:
            logits, value_logit = model(src, tgt_in)
            policy_loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), tgt_out.reshape(-1), ignore_index=PAD,
                                          reduction="sum") / max(n_tokens, 1)
            value_loss = (F.binary_cross_entropy_with_logits(value_logit, value_target, reduction="none")
                          * value_mask).sum() / max(n_values, 1.0)
            (policy_loss + config.value_weight * value_loss).backward()
            totals["policy_loss"] += policy_loss.item()
            totals["value_loss"] += value_loss.item()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    return {k: round(v / config.steps_per_iter, 4) for k, v in totals.items()}, step


def evaluate(problems: list, proposer, mode: str, budget: int, k: int = 8) -> dict:
    """Solve rate of a proposer on a list of ``Problem``s. mode: 'greedy' or 'search'."""
    make = GreedySearch if mode == "greedy" else BestFirstSearch
    searches = [make(p, budget=budget) for p in problems]
    run_searches(searches, proposer, k)
    solved = [s for s in searches if s.solved_node is not None]
    return {
        "solved": len(solved), "n": len(problems), "rate": round(len(solved) / max(1, len(problems)), 4),
        "mean_calls_solved": round(sum(s.calls for s in solved) / len(solved), 2) if solved else None,
    }


def run_dirs(run: str) -> tuple[pathlib.Path, pathlib.Path]:
    ckpt = ROOT / "checkpoints" / run
    logs = ROOT / "logs" / run
    ckpt.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    return ckpt, logs


def train(config: TrainConfig, resume: bool = False) -> dict:
    """Run (or resume) one training run. Returns the last log record."""
    began = time.time()
    device = pick_device(config.device)
    ckpt_dir, log_dir = run_dirs(config.run)
    rng = random.Random(config.seed)
    torch.manual_seed(config.seed)

    pool = ProblemPool(config.seed, config.per_tier, for_training=True)
    model = PolicyValueNet(ModelConfig(**config.model)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    buffer = ReplayBuffer(config.buffer_size)
    state = {"iteration": 0, "step": 0, "tier": config.start_tier, "tier_iters": 0, "ema": 0.0, "seconds": 0.0}

    last = ckpt_dir / "last.pt"
    if resume and last.exists():
        # weights_only=True for both files: they hold tensors and plain values, and a file from
        # someone else (a downloaded checkpoint put here to continue training) must not run code.
        payload = torch.load(last, map_location="cpu", weights_only=True)
        check_vocabulary(payload, last)
        model.load_state_dict(payload["model"])
        state = payload.get("state", state)
        if "optimizer" in payload and "rng" in payload:
            optimizer.load_state_dict(payload["optimizer"])
            rng.setstate(_as_rng_state(payload["rng"]))
        else:
            print(f"{last} is a weights-only export (no optimiser or random state): "
                  "continuing with a fresh optimiser and a fresh random stream")
        buffer_path = ckpt_dir / BUFFER_FILE
        if buffer_path.exists():
            stored = torch.load(buffer_path, map_location="cpu", weights_only=True)
            buffer.solve, buffer.hindsight, buffer.negative = ([tuple(tuple(part) for part in item) for item in store]
                                                               for store in stored)
        elif (ckpt_dir / "buffer.pkl").exists():
            print(f"{ckpt_dir / 'buffer.pkl'} is in the old pickle format and is not loaded; the replay buffer starts empty")
        print(f"resumed {config.run} at iteration {state['iteration']} (tier {state['tier']}, {len(buffer)} examples)")
    else:
        (log_dir / "config.json").write_text(json.dumps(asdict(config), indent=1))

    log_path = log_dir / "train.jsonl"
    print(f"run {config.run}: device {device}, {model.n_parameters():,} parameters, "
          f"train problems per tier {[len(v) for v in pool.train.values()]}, held out {[len(v) for v in pool.test.values()]}")
    uniform = UniformProposer(random.Random(config.seed + 1))
    record: dict = {}
    while state["iteration"] < config.iterations and time.time() - began < config.minutes * 60:
        tick = time.time()
        state["iteration"] += 1
        state["tier_iters"] += 1
        tier = state["tier"]

        # 1-2. self-play
        items = pool.sample_train(rng, tier, config.problems_per_iter)
        searches = [BestFirstSearch(item.problem(), budget=config.budget) for item in items]
        proposer = NeuralProposer(model, device, DIVERSE if config.diverse else config.temperature, config.n_uniform, rng,
                                  n_subterm=config.n_subterm)
        run_searches(searches, proposer, config.k)
        on_tier = [s for s, item in zip(searches, items) if item.tier == tier]
        rate = sum(s.solved_node is not None for s in on_tier) / max(1, len(on_tier))
        overall = sum(s.solved_node is not None for s in searches) / len(searches)
        state["ema"] = rate if state["tier_iters"] == 1 else 0.6 * state["ema"] + 0.4 * rate
        selfplay_seconds = time.time() - tick

        # 3-4. learn
        harvest(searches, buffer, rng, minimise=config.minimise, mirror=config.mirror)
        losses = {}
        if buffer.solve:
            losses, state["step"] = train_steps(model, optimizer, buffer, config, rng, device, state["step"])

        record = {
            "iteration": state["iteration"], "tier": tier, "selfplay_rate_tier": round(rate, 4),
            "selfplay_rate_all": round(overall, 4), "ema": round(state["ema"], 4),
            "mean_calls": round(sum(s.calls for s in searches) / len(searches), 1),
            "buffer": [len(buffer.solve), len(buffer.hindsight), len(buffer.negative)], **losses,
            "selfplay_s": round(selfplay_seconds, 1), "iter_s": round(time.time() - tick, 1),
        }
        if device.type == "mps":
            torch.mps.empty_cache()
            record["mps_gb"] = round(torch.mps.driver_allocated_memory() / 2**30, 2)

        # periodic held-out evaluation (greedy, no exploration)
        if state["iteration"] % config.eval_every == 0:
            eval_proposer = NeuralProposer(model, device, temperature=DIVERSE if config.diverse else 0.7)
            for t in range(1, tier + 1):
                problems = [g.problem() for g in pool.test[t][: config.eval_problems]]
                record[f"heldout_t{t}_greedy"] = evaluate(problems, eval_proposer, "greedy", config.eval_budget)["rate"]
                if state["iteration"] == config.eval_every:
                    record[f"uniform_t{t}_greedy"] = evaluate(problems, uniform, "greedy", config.eval_budget)["rate"]

        # 5. curriculum
        promote = state["tier_iters"] >= config.min_iters_per_tier and state["ema"] >= config.promote_at
        if (promote or state["tier_iters"] >= config.max_iters_per_tier) and tier < config.max_tier:
            state["tier"], state["tier_iters"] = tier + 1, 0
            record["promoted_to"] = tier + 1

        state["seconds"] += time.time() - tick
        record["total_minutes"] = round(state["seconds"] / 60, 2)
        with open(log_path, "a") as fh:
            fh.write(json.dumps(record) + "\n")
        print(json.dumps(record), flush=True)
        save_checkpoint(last, model, {"optimizer": optimizer.state_dict(), "state": state, "rng": rng.getstate(),
                                      "train_config": asdict(config)})
        if state["iteration"] % 5 == 0:
            _save_buffer(ckpt_dir, buffer)
    _save_buffer(ckpt_dir, buffer)
    return record


BUFFER_FILE = "buffer.pt"


def _save_buffer(ckpt_dir, buffer: ReplayBuffer) -> None:
    """The replay buffer as plain lists of integers (no pickle of arbitrary objects, so it loads with weights_only)."""
    torch.save([[[list(part) for part in item] for item in store]
                for store in (buffer.solve, buffer.hindsight, buffer.negative)], ckpt_dir / BUFFER_FILE)


def _as_rng_state(stored):
    """``random.Random.getstate()`` as it comes back from a checkpoint: lists turned into the tuples setstate wants."""
    version, internal, gauss = stored
    return (version, tuple(internal), gauss)


TRUE_WORDS, FALSE_WORDS = ("true", "1", "yes", "on"), ("false", "0", "no", "off")


def apply_overrides(config: TrainConfig, items: list) -> None:
    """Apply ``KEY=VALUE`` overrides to a config, refusing anything that cannot be read exactly."""
    fields = sorted(asdict(config))
    for item in items:
        key, sep, value = item.partition("=")
        if not sep:
            raise ValueError(f"--set {item}: expected KEY=VALUE")
        if key not in fields or key == "model":
            hint = " (the model size is not set this way)" if key == "model" else ""
            raise ValueError(f"--set {item}: unknown setting{hint}; the settings are: {', '.join(f for f in fields if f != 'model')}")
        current = getattr(config, key)
        if isinstance(current, bool):
            word = value.strip().lower()
            if word not in TRUE_WORDS + FALSE_WORDS:
                raise ValueError(f"--set {item}: {key} is on or off; write {key}=true or {key}=false")
            setattr(config, key, word in TRUE_WORDS)
        else:
            try:
                setattr(config, key, type(current)(value))
            except ValueError:
                raise ValueError(f"--set {item}: {key} takes {type(current).__name__} values") from None


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="alphafe train", description="Self-play training (resumable).")
    parser.add_argument("--run", default="default", help="run name (checkpoints/<run>, logs/<run>)")
    parser.add_argument("--resume", action="store_true", help="continue from checkpoints/<run>/last.pt")
    parser.add_argument("--minutes", type=float, default=28.0, help="wall-clock limit for this invocation")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                        help="override any TrainConfig field, e.g. --set budget=64")
    args = parser.parse_args(argv)
    config = TrainConfig(run=args.run, minutes=args.minutes, iterations=args.iterations)
    config_path = ROOT / "logs" / args.run / "config.json"
    if args.resume and config_path.exists():
        saved = json.loads(config_path.read_text())
        config = TrainConfig(**{**saved, "minutes": args.minutes, "iterations": args.iterations})
    try:
        apply_overrides(config, args.set)
    except ValueError as err:
        parser.error(str(err))
    if args.set:
        print("settings: " + ", ".join(f"{key}={getattr(config, key)}" for key in sorted(asdict(config)) if key != "model"))
    train(config, resume=args.resume)


if __name__ == "__main__":
    main()
