from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from scripts.tt_ops import build_random_cores, contract_full, reconstruct_full, tt_contract

DEFAULT_OUTPUT = Path("docs/assets/demo_output.txt")


def run_demo(seed: int, dims: tuple[int, ...], ranks: tuple[int, ...]) -> dict[str, float | str]:
    rng = np.random.default_rng(seed)
    cores = build_random_cores(rng, dims, ranks)
    vectors = [rng.standard_normal((n,)) for n in dims]

    tt_value = tt_contract(cores, vectors)
    full = reconstruct_full(cores)
    full_value = contract_full(full, vectors)

    abs_error = abs(tt_value - full_value)
    rel_error = abs_error / (abs(full_value) + 1e-12)

    return {
        "seed": str(seed),
        "dims": ",".join(str(n) for n in dims),
        "ranks": ",".join(str(r) for r in ranks),
        "tt_value": f"{tt_value:.6e}",
        "full_value": f"{full_value:.6e}",
        "abs_error": f"{abs_error:.6e}",
        "rel_error": f"{rel_error:.6e}",
    }


def write_output(output_path: Path, payload: dict[str, float | str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "demo_tt",
        f"seed: {payload['seed']}",
        f"dims: {payload['dims']}",
        f"ranks: {payload['ranks']}",
        f"tt_value: {payload['tt_value']}",
        f"full_value: {payload['full_value']}",
        f"abs_error: {payload['abs_error']}",
        f"rel_error: {payload['rel_error']}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo de contraccion TT en CPU.")
    parser.add_argument("--seed", type=int, default=0, help="Seed reproducible.")
    parser.add_argument(
        "--dims",
        type=str,
        default="4,5,3",
        help="Dimensiones separadas por coma.",
    )
    parser.add_argument(
        "--ranks",
        type=str,
        default="1,2,2,1",
        help="Rangos TT separados por coma.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta de salida.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dims = tuple(int(x) for x in args.dims.split(",") if x)
    ranks = tuple(int(x) for x in args.ranks.split(",") if x)
    payload = run_demo(args.seed, dims, ranks)
    write_output(args.output, payload)


if __name__ == "__main__":
    main()
