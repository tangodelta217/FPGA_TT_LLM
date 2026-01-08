from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np


def _as_int_tuple(values: Sequence[int], name: str) -> tuple[int, ...]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of ints")
    try:
        result = tuple(int(v) for v in values)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain only ints") from exc
    if not result:
        raise ValueError(f"{name} must be non-empty")
    if any(v <= 0 for v in result):
        raise ValueError(f"{name} must contain positive ints")
    return result


def _prod(values: Iterable[int]) -> int:
    prod = 1
    for value in values:
        prod *= int(value)
    return int(prod)


def tensorize_matrix(
    weights: np.ndarray, dims_out: Sequence[int], dims_in: Sequence[int]
) -> np.ndarray:
    weights = np.asarray(weights)
    if weights.ndim != 2:
        raise ValueError("weights must be a 2D array")

    dims_out_t = _as_int_tuple(dims_out, "dims_out")
    dims_in_t = _as_int_tuple(dims_in, "dims_in")
    if len(dims_out_t) != len(dims_in_t):
        raise ValueError("dims_out and dims_in must have the same length")

    out_size = _prod(dims_out_t)
    in_size = _prod(dims_in_t)
    if weights.shape != (out_size, in_size):
        raise ValueError(
            "weights shape must match product of dims_out and dims_in: "
            f"got {weights.shape}, expected ({out_size}, {in_size})"
        )

    tensor = weights.reshape(*dims_out_t, *dims_in_t)
    order = []
    d = len(dims_out_t)
    for i in range(d):
        order.extend([i, i + d])
    return tensor.transpose(order)


def _normalize_ranks(ranks: Sequence[int] | int, d: int) -> tuple[int, ...]:
    if isinstance(ranks, int):
        if ranks < 1:
            raise ValueError("rank must be >= 1")
        rank_list = [1] + [int(ranks)] * (d - 1) + [1]
    else:
        rank_list = [int(r) for r in ranks]
        if len(rank_list) != d + 1:
            raise ValueError("ranks must have length d + 1")
        if rank_list[0] != 1 or rank_list[-1] != 1:
            raise ValueError("first and last rank must be 1")
        if any(r < 1 for r in rank_list):
            raise ValueError("ranks must be >= 1")
    return tuple(rank_list)


def tt_svd_matrix(
    weights: np.ndarray,
    dims_out: Sequence[int],
    dims_in: Sequence[int],
    ranks: Sequence[int] | int,
) -> list[np.ndarray]:
    dims_out_t = _as_int_tuple(dims_out, "dims_out")
    dims_in_t = _as_int_tuple(dims_in, "dims_in")
    if len(dims_out_t) != len(dims_in_t):
        raise ValueError("dims_out and dims_in must have the same length")

    d = len(dims_out_t)
    rank_list = _normalize_ranks(ranks, d)

    weights = np.asarray(weights)
    tensor = tensorize_matrix(weights, dims_out_t, dims_in_t)

    if d == 1:
        core = tensor.reshape(1, dims_out_t[0], dims_in_t[0], 1)
        return [core]

    cores: list[np.ndarray] = []
    curr = tensor
    r_prev = 1

    for k in range(d - 1):
        n_k = dims_out_t[k]
        m_k = dims_in_t[k]
        curr = curr.reshape(r_prev * n_k * m_k, -1)
        u, s, vh = np.linalg.svd(curr, full_matrices=False)
        r_next = min(rank_list[k + 1], s.size)
        if r_next < 1:
            raise ValueError("rank truncation produced an invalid rank")

        core = u[:, :r_next].reshape(r_prev, n_k, m_k, r_next)
        cores.append(core)

        curr = (s[:r_next, None] * vh[:r_next, :])
        remaining_shape: list[int] = []
        for j in range(k + 1, d):
            remaining_shape.extend([dims_out_t[j], dims_in_t[j]])
        curr = curr.reshape(r_next, *remaining_shape)
        r_prev = r_next

    core = curr.reshape(r_prev, dims_out_t[-1], dims_in_t[-1], 1)
    cores.append(core)
    return cores


def tt_matvec(cores: Sequence[np.ndarray], x: np.ndarray) -> np.ndarray:
    if not cores:
        raise ValueError("cores list is empty")

    x = np.asarray(x)
    if x.ndim != 1:
        raise ValueError("x must be a 1D vector")

    dims_in = [core.shape[2] for core in cores]
    in_size = _prod(dims_in)
    if x.size != in_size:
        raise ValueError(f"x length must be {in_size}")

    for idx, core in enumerate(cores):
        if core.ndim != 4:
            raise ValueError(f"core {idx} must be 4D (r, n, m, r_next)")

    x_tensor = x.reshape(*dims_in)
    phi = x_tensor.reshape(1, *dims_in)

    for idx, core in enumerate(cores):
        if phi.shape[0] != core.shape[0]:
            raise ValueError(f"rank mismatch at core {idx}")
        if phi.shape[1] != core.shape[2]:
            raise ValueError(f"input mode mismatch at core {idx}")

        result = np.tensordot(core, phi, axes=([0, 2], [0, 1]))
        axes = [1] + list(range(2, result.ndim)) + [0]
        phi = np.transpose(result, axes=axes)

    y_tensor = np.squeeze(phi, axis=0)
    return y_tensor.reshape(-1)


def tt_cores_to_matrix(cores: Sequence[np.ndarray]) -> np.ndarray:
    if not cores:
        raise ValueError("cores list is empty")

    for idx, core in enumerate(cores):
        if core.ndim != 4:
            raise ValueError(f"core {idx} must be 4D (r, n, m, r_next)")

    tensor = cores[0]
    for idx, core in enumerate(cores[1:], start=1):
        if tensor.shape[-1] != core.shape[0]:
            raise ValueError(f"rank mismatch between core {idx - 1} and {idx}")
        tensor = np.tensordot(tensor, core, axes=([-1], [0]))

    if tensor.shape[0] != 1 or tensor.shape[-1] != 1:
        raise ValueError("first and last TT ranks must be 1")

    tensor = np.squeeze(tensor, axis=(0, -1))
    d = len(cores)
    order = list(range(0, 2 * d, 2)) + list(range(1, 2 * d, 2))
    tensor = tensor.transpose(order)

    dims_out = [core.shape[1] for core in cores]
    dims_in = [core.shape[2] for core in cores]
    return tensor.reshape(_prod(dims_out), _prod(dims_in))
