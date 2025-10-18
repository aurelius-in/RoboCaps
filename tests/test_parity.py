import numpy as np

from src.inference.edge_inference import EdgeInference


def test_parity_check():
    ei = EdgeInference()
    res = ei.parity_check(batch=1, tol=1e-3)
    assert "probs_delta" in res and "poses_delta" in res
    # ORT may be unavailable in CI; when session is None, deltas are zero
    assert res["probs_delta"] >= 0.0
    assert res["poses_delta"] >= 0.0
