from __future__ import annotations

from typing import Dict

import torch


@torch.no_grad()
def evaluate(outputs: Dict[str, torch.Tensor], targets: Dict[str, torch.Tensor]) -> Dict[str, float]:
    logits = outputs["part_logits"]
    poses_pred = outputs["poses"]
    labels = targets["part_labels"]
    poses_gt = targets["poses"]

    probs = torch.sigmoid(logits)
    confidence = probs.mean().item()
    pose_l1 = (poses_pred - poses_gt).abs().mean().item()
    # Naive AP proxy: fraction above 0.5 matching positive labels
    pred_pos = (probs > 0.5).float()
    ap_proxy = (pred_pos * labels).sum().item() / (labels.sum().item() + 1e-6)
    return {"confidence": confidence, "pose_l1": pose_l1, "ap_proxy": ap_proxy}
