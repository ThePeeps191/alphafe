import random

import pytest
import torch

from alphafe.checker import Problem
from alphafe.env import start
from alphafe.model import ModelConfig, NeuralProposer, PolicyValueNet, load_model, pad_batch, save_checkpoint
from alphafe.search import BestFirstSearch, run_searches
from alphafe.tokenizer import BOS, EOS, PAD, decode_move, encode_state

TINY = ModelConfig(d_model=32, n_heads=2, enc_layers=1, dec_layers=1, d_ff=64)
CPU = torch.device("cpu")


def view_of(equation):
    state, _ = start(Problem.parse(equation))
    return encode_state(state)


def test_forward_shapes():
    model = PolicyValueNet(TINY)
    src = pad_batch([view_of("f(x+y) = f(x) + y").tokens, view_of("f(xy) = x*f(y)").tokens])
    tgt = torch.tensor([[BOS, 5, 6], [BOS, 7, PAD]])
    logits, value = model(src, tgt)
    assert logits.shape == (2, 3, TINY.vocab_size) and value.shape == (2,)
    assert torch.isfinite(logits).all() and torch.isfinite(value).all()


def test_default_model_size_is_in_the_planned_range():
    assert 1_000_000 <= PolicyValueNet().n_parameters() <= 5_000_000


def test_pad_batch_rounds_width_up():
    batch = pad_batch([[1, 2, 3], [4]], multiple=8)
    assert batch.shape == (2, 8) and batch[1, 1] == PAD


def test_proposals_are_well_formed_moves():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU, n_uniform=2, rng=random.Random(0))
    views = [view_of("f(x+y) = f(x) + y"), view_of("f(x)f(y) = f(x+y) + xy"), view_of("f(xy) = x*f(y)")]
    proposals = proposer.propose(views, k=6)
    assert len(proposals) == 3
    for view, props in zip(views, proposals):
        assert 1 <= len(props) <= 6
        for ids, logp in props:
            assert ids[-1] == EOS and logp <= 0
            decode_move(ids, view)          # must not raise
    values = proposer.values(views)
    assert len(values) == 3 and all(0 <= v <= 1 for v in values)


def test_untrained_network_can_drive_search():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU)
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=300)
    run_searches([search], proposer, k=8)
    assert search.done and search.calls <= 300


def test_checkpoint_round_trip(tmp_path):
    model = PolicyValueNet(TINY)
    path = tmp_path / "m.pt"
    save_checkpoint(path, model, {"note": "hello"})
    loaded, payload = load_model(path, CPU)
    assert payload["note"] == "hello" and loaded.config == TINY
    for a, b in zip(model.parameters(), loaded.parameters()):
        assert torch.equal(a, b)


def test_value_guided_search_with_network():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU)
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=120, value_weight=1.0)
    run_searches([search], proposer, k=8)
    assert search.done and search.calls <= 120 and len(search.nodes) > 1
