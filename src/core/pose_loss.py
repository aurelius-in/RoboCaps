from __future__ import annotations

from typing import Dict

import torch
import torch.nn as nn


class PoseLoss(nn.Module):
    """Composite loss: part confidence margin + pose consistency + equivariance regularizer.

    This is a simplified version suitable for initial training.
    """

    def __init__(self, margin: float = 0.2, pose_weight: float = 1.0, equiv_weight: float = 0.1) -> None:
        super().__init__()
        self.margin = margin
        self.pose_weight = pose_weight
        self.equiv_weight = equiv_weight
        self.bce = nn.BCEWithLogitsLoss()

    def forward(
        self,
        outputs: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor],
        equivariant_outputs: Dict[str, torch.Tensor] | None = None,
    ) -> Dict[str, torch.Tensor]:
        """Compute composite loss.

        Args:
            outputs: model outputs with keys `part_logits`, `poses`.
            targets: tensors with keys `part_labels` (b,np) and `poses` (b,np,3).
            equivariant_outputs: optional outputs from transformed inputs for equivariance.
        Returns:
            dict with per-term losses and total.
        """
        logits = outputs["part_logits"]
        pred_poses = outputs["poses"]
        labels = targets["part_labels"].float()
        gt_poses = targets["poses"]

        # Part confidence (binary) loss
        part_loss = self.bce(logits, labels)

        # Pose L1, masked by positives
        pos_mask = (labels > 0.5).unsqueeze(-1)
        if pos_mask.any():
            pose_l1 = (pred_poses[pos_mask] - gt_poses[pos_mask]).abs().mean()
        else:
            pose_l1 = torch.zeros((), device=logits.device)

        # Equivariance regularization (if provided): encourage consistent relative poses
        if equivariant_outputs is not None:
            eq_pred = equivariant_outputs["poses"].detach()
            # Simple consistency: minimize difference
            equiv_loss = (pred_poses - eq_pred).abs().mean()
        else:
            equiv_loss = torch.zeros((), device=logits.device)

        total = part_loss + self.pose_weight * pose_l1 + self.equiv_weight * equiv_loss
        return {
            "loss": total,
            "part_loss": part_loss.detach(),
            "pose_l1": pose_l1.detach(),
            "equiv_loss": equiv_loss.detach(),
        }
