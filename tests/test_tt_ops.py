import numpy as np
from scripts.tt_ops import build_random_cores, contract_full, reconstruct_full, tt_contract


def test_tt_contract_matches_full() -> None:
    rng = np.random.default_rng(0)
    dims = (3, 4, 2)
    ranks = (1, 2, 2, 1)
    cores = build_random_cores(rng, dims, ranks)
    vectors = [rng.standard_normal((n,)) for n in dims]

    tt_value = tt_contract(cores, vectors)
    full = reconstruct_full(cores)
    full_value = contract_full(full, vectors)

    assert np.isclose(tt_value, full_value, rtol=1e-10, atol=1e-10)
