import numpy as np
from ml.tt import tt_matvec, tt_svd_matrix


def test_tt_matvec_matches_dense_full_rank() -> None:
    rng = np.random.default_rng(0)
    dims_out = (2, 2)
    dims_in = (2, 2)
    out_dim = int(np.prod(dims_out))
    in_dim = int(np.prod(dims_in))

    weights = rng.standard_normal((out_dim, in_dim))
    x = rng.standard_normal((in_dim,))

    cores = tt_svd_matrix(weights, dims_out, dims_in, ranks=(1, 4, 1))
    y_tt = tt_matvec(cores, x)
    y_dense = weights @ x

    assert np.allclose(y_tt, y_dense, rtol=1e-10, atol=1e-10)


def test_tt_matvec_shapes_and_small_ranks() -> None:
    rng = np.random.default_rng(1)
    dims_out = (2, 2)
    dims_in = (2, 2)
    out_dim = int(np.prod(dims_out))
    in_dim = int(np.prod(dims_in))

    weights = rng.standard_normal((out_dim, in_dim))
    x = rng.standard_normal((in_dim,))

    cores = tt_svd_matrix(weights, dims_out, dims_in, ranks=(1, 1, 1))
    y_tt = tt_matvec(cores, x)

    assert len(cores) == len(dims_out)
    assert y_tt.shape == (out_dim,)


def test_tt_matvec_raises_on_bad_input() -> None:
    rng = np.random.default_rng(2)
    dims_out = (2, 2)
    dims_in = (2, 2)
    weights = rng.standard_normal((4, 4))

    cores = tt_svd_matrix(weights, dims_out, dims_in, ranks=(1, 2, 1))
    bad_x = rng.standard_normal((5,))

    try:
        tt_matvec(cores, bad_x)
        raised = False
    except ValueError:
        raised = True

    assert raised
