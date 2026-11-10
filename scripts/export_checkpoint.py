"""Write a weights-only copy of a training checkpoint, for sharing.

    .venv/bin/python scripts/export_checkpoint.py checkpoints/v2/last.pt out/alphafe-v2.pt

A training checkpoint also holds the optimiser and random-number state, which
only matter for resuming. The exported file is a third of the size and holds
tensors and plain values only. Prints the SHA-256 to publish next to it.
"""
import hashlib
import pathlib
import sys

from alphafe.model import export_checkpoint

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source, target = map(pathlib.Path, sys.argv[1:])
    target.parent.mkdir(parents=True, exist_ok=True)
    slim = export_checkpoint(source, target)
    n = sum(t.numel() for t in slim["model"].values())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"{target}: {n:,} parameters, {target.stat().st_size / 1e6:.1f} MB, keys {sorted(slim)}")
    print(f"sha256 {digest}")
