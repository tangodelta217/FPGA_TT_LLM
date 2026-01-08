from __future__ import annotations

import argparse
import csv
import statistics
import time
from pathlib import Path
from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from ml.tt import tt_cores_to_matrix, tt_matvec, tt_svd_matrix

DEFAULT_CSV = Path("docs/assets/bench_results.csv")
DEFAULT_PNG = Path("docs/assets/bench_tradeoff.png")
DEFAULT_KPI = Path("docs/assets/kpi_table.md")


def _format_ranks(ranks: Sequence[int]) -> str:
    return "-".join(str(r) for r in ranks)


def _format_dims(dims: Sequence[int]) -> str:
    return "x".join(str(d) for d in dims)


def _median_time_us(func: Callable[[], np.ndarray], runs: int) -> float:
    times: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    return statistics.median(times) * 1e6


def _compression_bytes(cores: Sequence[np.ndarray]) -> int:
    return int(sum(core.nbytes for core in cores))


def build_random_tt_cores(
    rng: np.random.Generator,
    dims_out: Sequence[int],
    dims_in: Sequence[int],
    ranks: Sequence[int],
) -> list[np.ndarray]:
    if len(dims_out) != len(dims_in):
        raise ValueError("dims_out and dims_in must have the same length")
    if len(ranks) != len(dims_out) + 1:
        raise ValueError("ranks must have length d + 1")
    if ranks[0] != 1 or ranks[-1] != 1:
        raise ValueError("first and last rank must be 1")
    if any(r < 1 for r in ranks):
        raise ValueError("ranks must be >= 1")

    cores: list[np.ndarray] = []
    for i, (n_out, n_in) in enumerate(zip(dims_out, dims_in)):
        r0 = ranks[i]
        r1 = ranks[i + 1]
        cores.append(rng.standard_normal((r0, n_out, n_in, r1)))
    return cores


def write_csv(output_path: Path, rows: list[dict[str, float | str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "comp_ratio",
        "comp_pct",
        "rel_l2",
        "max_abs",
        "dense_us",
        "tt_us",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_kpi_table(
    output_path: Path,
    rows: list[dict[str, float | str]],
    context: str,
    base_info: str,
    runs: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# KPI demo TT (CPU)",
        context,
        base_info,
        f"Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de {runs} repeticiones.",
        "",
        "| rank | comp_ratio | comp_pct | rel_l2 | max_abs | dense_us | tt_us |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            (
                "| {rank} | {comp_ratio:.2f} | {comp_pct:.1f}% | {rel_l2:.3e} | "
                "{max_abs:.3e} | {dense_us:.2f} | {tt_us:.2f} |"
            ).format(**row)
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tradeoff_plot(
    output_path: Path,
    rank_values: Sequence[int],
    rel_l2: Sequence[float],
    comp_ratio: Sequence[float],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))

    axes[0].plot(rank_values, rel_l2, marker="o")
    axes[0].set_xlabel("rank")
    axes[0].set_ylabel("error rel_l2")
    axes[0].set_yscale("log")
    axes[0].grid(True, linestyle="--", alpha=0.4)

    axes[1].plot(rank_values, comp_ratio, marker="o")
    axes[1].set_xlabel("rank")
    axes[1].set_ylabel("compresion (dense/TT)")
    axes[1].grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmarks TT para capa lineal.")
    parser.add_argument("--seed", type=int, default=0, help="Semilla reproducible.")
    parser.add_argument("--runs", type=int, default=40, help="Repeticiones para medianas.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Salida CSV.")
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG, help="Salida grafico.")
    parser.add_argument("--kpi", type=Path, default=DEFAULT_KPI, help="Salida KPI.")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Modo rapido para CI (menos ranks y repeticiones).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dims_out = (4, 4, 4, 4)
    dims_in = (4, 4, 4, 4)
    rank_values = [2, 4, 8, 16]
    base_ranks = (1, 8, 8, 8, 1)
    runs = args.runs

    if args.quick:
        rank_values = [2, 4]
        base_ranks = (1, 4, 4, 4, 1)
        runs = 12

    rng = np.random.default_rng(args.seed)
    base_cores = build_random_tt_cores(rng, dims_out, dims_in, base_ranks)
    weights = tt_cores_to_matrix(base_cores)
    x = rng.standard_normal((weights.shape[1],))

    def dense_func() -> np.ndarray:
        return weights @ x

    dense_us = _median_time_us(dense_func, runs)
    y_dense = dense_func()

    rows: list[dict[str, float | str]] = []
    rel_l2_values: list[float] = []
    comp_ratio_values: list[float] = []

    for r in rank_values:
        ranks = (1, r, r, r, 1)
        cores = tt_svd_matrix(weights, dims_out, dims_in, ranks)
        y_tt = tt_matvec(cores, x)

        rel_l2 = float(np.linalg.norm(y_tt - y_dense) / (np.linalg.norm(y_dense) + 1e-12))
        max_abs = float(np.max(np.abs(y_tt - y_dense)))

        def tt_func() -> np.ndarray:
            return tt_matvec(cores, x)

        tt_us = _median_time_us(tt_func, runs)
        dense_bytes = int(weights.nbytes)
        tt_bytes = _compression_bytes(cores)
        comp_ratio = dense_bytes / tt_bytes
        comp_pct = 100.0 * (1.0 - (tt_bytes / dense_bytes))

        rows.append(
            {
                "rank": _format_ranks(ranks),
                "comp_ratio": comp_ratio,
                "comp_pct": comp_pct,
                "rel_l2": rel_l2,
                "max_abs": max_abs,
                "dense_us": dense_us,
                "tt_us": tt_us,
            }
        )
        rel_l2_values.append(rel_l2)
        comp_ratio_values.append(comp_ratio)

    context = (
        "Contexto: dims_out={dims_out}, dims_in={dims_in}, ranks={ranks}, "
        "repeticiones={runs}, semilla={seed}"
    ).format(
        dims_out=_format_dims(dims_out),
        dims_in=_format_dims(dims_in),
        ranks="|".join(_format_ranks((1, r, r, r, 1)) for r in rank_values),
        runs=runs,
        seed=args.seed,
    )
    base_info = f"Modelo sintetico: pesos generados con TT base rank={_format_ranks(base_ranks)}."

    write_csv(args.csv, rows)
    write_tradeoff_plot(args.png, rank_values, rel_l2_values, comp_ratio_values)
    write_kpi_table(args.kpi, rows, context, base_info, runs)


if __name__ == "__main__":
    main()
