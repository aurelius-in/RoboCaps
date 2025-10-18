import numpy as np
from fastapi.testclient import TestClient

from src.inference.api_server import app


def test_healthz():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_infer_array():
    client = TestClient(app)
    arr = (np.random.rand(1, 3, 224, 224).astype(np.float32)).flatten().tolist()
    r = client.post("/infer-array", json={"array": arr, "batch": 1})
    assert r.status_code == 200
    data = r.json()
    assert "part_probs" in data and "poses" in data
