import torch

from src.utils.metrics import add_metric, add_s_metric


def test_add_metrics_non_negative():
    pts = torch.zeros(10, 3)
    assert add_metric(pts, pts).item() == 0.0
    assert add_s_metric(pts, pts).item() == 0.0
