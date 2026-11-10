import json
import random
import shutil

import pytest
import torch

from alphafe import train as train_module
from alphafe.checker import Problem
from alphafe.generate import benchmark_keys
from alphafe.search import BestFirstSearch, UniformProposer, run_searches
from alphafe.tokenizer import EOS, TOKEN_ID
from alphafe.train import ProblemPool, ReplayBuffer, TrainConfig, harvest, make_batch, train

TINY_MODEL = dict(d_model=32, n_heads=2, enc_layers=1, dec_layers=1, d_ff=64, dropout=0.0, vocab_size=len(TOKEN_ID),
                  max_src=448, max_tgt=56)


def test_pool_split_is_disjoint_and_excludes_benchmarks():
    pool = ProblemPool(seed=5, per_tier=60)
    train_keys = {g.key for items in pool.train.values() for g in items}
    test_keys = {g.key for items in pool.test.values() for g in items}
    assert train_keys and test_keys and not train_keys & test_keys
    assert not (train_keys | test_keys) & benchmark_keys()
    rng = random.Random(0)
    sampled = pool.sample_train(rng, 3, 200)
    assert all(g.split == "train" and g.tier <= 3 for g in sampled)


def test_harvest_builds_the_three_kinds_of_examples():
    rng = random.Random(0)
    solved = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=300)
    failed = BestFirstSearch(Problem.parse("f(x+y) + f(x-y) = 2f(x) + 2f(y)", "Q"), budget=30)
    run_searches([solved, failed], UniformProposer(rng), k=8)
    assert solved.solved_node is not None and failed.solved_node is None
    buffer = ReplayBuffer(1000)
    harvest([solved, failed], buffer, rng)
    assert len(buffer.solve) == len(solved.solution_path()) - 1 >= 1
    assert buffer.negative and buffer.hindsight
    for src, tgt in buffer.solve + buffer.hindsight:
        assert tgt[-1] == EOS
    assert all(src[2] == TOKEN_ID["SOLVE"] for src, _ in buffer.solve)
    assert all(src[2] == TOKEN_ID["GOAL"] for src, _ in buffer.hindsight)
    config = TrainConfig(batch_size=16)
    src, tgt_in, tgt_out, value, mask = make_batch(buffer, config, rng, torch.device("cpu"))
    assert src.shape[0] == tgt_in.shape[0] == 16 and tgt_in.shape == tgt_out.shape


@pytest.mark.slow
def test_training_runs_checkpoints_and_resumes(tmp_path, monkeypatch):
    monkeypatch.setattr(train_module, "ROOT", tmp_path)
    config = TrainConfig(run="t", per_tier=40, iterations=2, problems_per_iter=12, budget=16, steps_per_iter=3,
                         batch_size=8, eval_every=1, eval_problems=4, device="cpu", model=TINY_MODEL, minutes=5)
    record = train(config)
    assert record["iteration"] == 2 and "heldout_t1_greedy" in record
    assert (tmp_path / "checkpoints" / "t" / "last.pt").exists()
    assert (tmp_path / "checkpoints" / "t" / "buffer.pkl").exists()
    lines = (tmp_path / "logs" / "t" / "train.jsonl").read_text().splitlines()
    assert len(lines) == 2 and json.loads(lines[0])["iteration"] == 1
    config.iterations = 3
    resumed = train(config, resume=True)
    assert resumed["iteration"] == 3
