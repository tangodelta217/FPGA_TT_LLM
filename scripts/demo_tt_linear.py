from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
from ml.tt import tt_cores_to_matrix, tt_matvec, tt_svd_matrix

DEFAULT_OUTPUT = Path("docs/assets/demo_output.txt")
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


def _write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_demo(
    dims_out: tuple[int, ...],
    dims_in: tuple[int, ...],
    ranks_list: list[tuple[int, ...]],
    base_ranks: tuple[int, ...],
    seed: int,
    runs: int,
) -> tuple[list[dict[str, float | str]], float, str, str]:
    rng = np.random.default_rng(seed)
    out_dim = int(np.prod(dims_out))
    in_dim = int(np.prod(dims_in))

    weights_seed = rng.standard_normal((out_dim, in_dim))
    base_cores = tt_svd_matrix(weights_seed, dims_out, dims_in, base_ranks)
    weights = tt_cores_to_matrix(base_cores)
    x = rng.standard_normal((in_dim,))

    def dense_func() -> np.ndarray:
        return weights @ x

    dense_us = _median_time_us(dense_func, runs)
    y_dense = dense_func()

    rows: list[dict[str, float | str]] = []
    for ranks in ranks_list:
        cores = tt_svd_matrix(weights, dims_out, dims_in, ranks)
        y_tt = tt_matvec(cores, x)

        rel_l2 = np.linalg.norm(y_tt - y_dense) / (np.linalg.norm(y_dense) + 1e-12)
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

    context = (
        "Contexto: dims_out={dims_out}, dims_in={dims_in}, ranks={ranks}, "
        "repeticiones={runs}, semilla={seed}"
    ).format(
        dims_out=_format_dims(dims_out),
        dims_in=_format_dims(dims_in),
        ranks="|".join(_format_ranks(r) for r in ranks_list),
        runs=runs,
        seed=seed,
    )
    base_info = f"Modelo sintetico: pesos generados con TT base rank={_format_ranks(base_ranks)}."
    return rows, dense_us, context, base_info


def write_outputs(
    rows: list[dict[str, float | str]],
    dense_us: float,
    context: str,
    base_info: str,
    output_path: Path,
    kpi_path: Path,
    runs: int,
) -> None:
    header_lines = [
        "Demo TT para capa lineal",
        context,
        base_info,
        f"Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de {runs} repeticiones.",
        f"Dense baseline (us): {dense_us:.2f}",
        "",
        "| rank | comp_ratio | comp_pct | rel_l2 | max_abs | tt_us |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    table_lines = []
    for row in rows:
        table_lines.append(
            (
                "| {rank} | {comp_ratio:.2f} | {comp_pct:.1f}% | {rel_l2:.3e} | "
                "{max_abs:.3e} | {tt_us:.2f} |"
            ).format(**row)
        )

    output_lines = header_lines + table_lines
    _write_text(output_path, output_lines)

    kpi_lines = [
        "# KPI demo TT (CPU)",
        context,
        base_info,
        f"Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de {runs} repeticiones.",
        "",
        "| rank | comp_ratio | comp_pct | rel_l2 | max_abs | dense_us | tt_us |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        kpi_lines.append(
            (
                "| {rank} | {comp_ratio:.2f} | {comp_pct:.1f}% | {rel_l2:.3e} | "
                "{max_abs:.3e} | {dense_us:.2f} | {tt_us:.2f} |"
            ).format(**row)
        )
    _write_text(kpi_path, kpi_lines)

    print("\n".join(output_lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo TT para capa lineal.")
    parser.add_argument("--seed", type=int, default=0, help="Semilla reproducible.")
    parser.add_argument("--runs", type=int, default=30, help="Repeticiones para medianas.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Salida demo.")
    parser.add_argument("--kpi", type=Path, default=DEFAULT_KPI, help="Salida KPIs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dims_out = (4, 4, 4, 4)
    dims_in = (4, 4, 4, 4)
    ranks_list = [
        (1, 2, 2, 2, 1),
        (1, 4, 4, 4, 1),
        (1, 8, 8, 8, 1),
    ]
    base_ranks = (1, 4, 4, 4, 1)

    rows, dense_us, context, base_info = run_demo(
        dims_out=dims_out,
        dims_in=dims_in,
        ranks_list=ranks_list,
        base_ranks=base_ranks,
        seed=args.seed,
        runs=args.runs,
    )
    write_outputs(rows, dense_us, context, base_info, args.output, args.kpi, args.runs)


if __name__ == "__main__":
    main()
