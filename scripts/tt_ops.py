from __future__ import annotations

from typing import Sequence

import numpy as np


def build_random_cores(
    rng: np.random.Generator, dims: Sequence[int], ranks: Sequence[int]
) -> list[np.ndarray]:
    if len(ranks) != len(dims) + 1:
        raise ValueError("ranks must have len(dims) + 1")

    cores: list[np.ndarray] = []
    for i, n in enumerate(dims):
        r0, r1 = ranks[i], ranks[i + 1]
        cores.append(rng.standard_normal((r0, n, r1)))
    return cores


def tt_contract(cores: Sequence[np.ndarray], vectors: Sequence[np.ndarray]) -> float:
    if len(cores) != len(vectors):
        raise ValueError("cores and vectors must have the same length")

    acc: np.ndarray | None = None
    for idx, (core, vec) in enumerate(zip(cores, vectors)):
        if core.ndim != 3:
            raise ValueError(f"core {idx} must be 3D (r_prev, n, r_next)")
        if vec.ndim != 1:
            raise ValueError(f"vector {idx} must be 1D")
        if core.shape[1] != vec.shape[0]:
            raise ValueError(
                f"shape mismatch at core {idx}: core n={core.shape[1]} vector n={vec.shape[0]}"
            )

        mat = np.tensordot(core, vec, axes=([1], [0]))
        acc = mat if acc is None else acc @ mat

    if acc is None:
        raise ValueError("cores list is empty")
    return float(np.squeeze(acc))


def reconstruct_full(cores: Sequence[np.ndarray]) -> np.ndarray:
    if not cores:
        raise ValueError("cores list is empty")
    if cores[0].shape[0] != 1 or cores[-1].shape[2] != 1:
        raise ValueError("first and last TT ranks must be 1")

    tensor = cores[0]
    for idx, core in enumerate(cores[1:], start=1):
        if tensor.shape[-1] != core.shape[0]:
            raise ValueError(f"rank mismatch between core {idx - 1} and {idx}")
        tensor = np.tensordot(tensor, core, axes=([-1], [0]))

    return np.squeeze(tensor, axis=(0, -1))


def contract_full(full: np.ndarray, vectors: Sequence[np.ndarray]) -> float:
    result = full
    for idx, vec in enumerate(vectors):
        if vec.ndim != 1:
            raise ValueError(f"vector {idx} must be 1D")
        if result.shape[0] != vec.shape[0]:
            raise ValueError(
                f"shape mismatch at mode {idx}: tensor n={result.shape[0]} vector n={vec.shape[0]}"
            )
        result = np.tensordot(result, vec, axes=([0], [0]))

    return float(result)
