from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path

import numpy as np

from scripts.tt_ops import build_random_cores, tt_contract

DEFAULT_OUTPUT = Path("docs/assets/benchmarks.md")
DEFAULT_CASES = [
    ((4, 5, 3), (1, 2, 2, 1)),
    ((8, 8, 8), (1, 4, 4, 1)),
]


def bench_case(
    dims: tuple[int, ...], ranks: tuple[int, ...], runs: int, seed: int
) -> dict[str, float | str]:
    rng = np.random.default_rng(seed)
    cores = build_random_cores(rng, dims, ranks)
    vectors = [rng.standard_normal((n,)) for n in dims]

    tt_contract(cores, vectors)
    times: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        tt_contract(cores, vectors)
        times.append(time.perf_counter() - start)

    times_us = [t * 1e6 for t in times]
    return {
        "dims": "x".join(str(n) for n in dims),
        "ranks": "-".join(str(r) for r in ranks),
        "runs": runs,
        "median_us": statistics.median(times_us),
        "min_us": min(times_us),
        "max_us": max(times_us),
    }


def write_output(output_path: Path, rows: list[dict[str, float | str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Benchmarks CPU (NumPy)",
        "",
        "Resultados de contraccion TT en CPU. No representan rendimiento en FPGA.",
        "",
        "| dims | ranks | runs | median_us | min_us | max_us |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {dims} | {ranks} | {runs} | {median_us:.2f} | {min_us:.2f} | {max_us:.2f} |".format(
                **row
            )
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark CPU para contraccion TT.")
    parser.add_argument("--runs", type=int, default=20, help="Repeticiones por caso.")
    parser.add_argument("--seed", type=int, default=0, help="Seed reproducible.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Ruta de salida.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [bench_case(dims, ranks, args.runs, args.seed) for dims, ranks in DEFAULT_CASES]
    write_output(args.output, rows)


if __name__ == "__main__":
    main()
