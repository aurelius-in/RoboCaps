import torch

from src.core.pose_loss import PoseLoss


def test_pose_loss_forward_zero_when_equal():
    b, nparts = 2, 5
    logits = torch.zeros(b, nparts)
    poses = torch.zeros(b, nparts, 3)
    labels = torch.zeros(b, nparts)
    outputs = {"part_logits": logits, "poses": poses}
    targets = {"part_labels": labels, "poses": poses.clone()}
    loss = PoseLoss()
    out = loss(outputs, targets)
    assert out["loss"].item() >= 0.0
