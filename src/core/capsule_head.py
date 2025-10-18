from __future__ import annotations

from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .routing_attention import RoutingAttention


class AttentionRoutedCapsuleHead(nn.Module):
    """Capsule head producing part probabilities and pose parameters.

    Pose parameterization:
      - se2: (tx, ty, theta)
      - se3: (tx, ty, tz, qw, qx, qy, qz)
    """

    def __init__(
        self,
        input_dim: int,
        num_children: int,
        num_parts: int,
        num_heads: int = 4,
        hidden_dim: int = 256,
        pose_mode: str = "se2",
    ) -> None:
        super().__init__()
        assert pose_mode in {"se2", "se3"}
        self.num_parts = num_parts
        self.num_children = num_children
        self.pose_mode = pose_mode
        self.routing = RoutingAttention(input_dim=input_dim, num_parents=num_parts, num_heads=num_heads)
        self.mlp = nn.Sequential(
            nn.LayerNorm(input_dim),
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
        )
        self.logit_proj = nn.Linear(hidden_dim, 1)
        pose_out = 3 if pose_mode == "se2" else 7
        self.pose_proj = nn.Linear(hidden_dim, pose_out)

    def forward(self, child_tokens: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Compute part scores and poses.

        Args:
            child_tokens: (batch, num_children, input_dim)
        Returns:
            dict with:
                - part_logits: (batch, num_parts)
                - part_probs: (batch, num_parts)
                - poses: (batch, num_parts, P)
                - attn: (batch, heads, num_parts, num_children)
        """
        parents, attn = self.routing(child_tokens)  # (b,np,c), (b,h,np,nc)
        h = self.mlp(parents)  # (b,np,hidden)
        logits = self.logit_proj(h).squeeze(-1)  # (b,np)
        probs = torch.sigmoid(logits)
        poses = self.pose_proj(h)  # (b,np,P)
        if self.pose_mode == "se3":
            # Normalize quaternion part to unit length
            t = poses[..., :3]
            q = poses[..., 3:]
            q = q / (q.norm(dim=-1, keepdim=True) + 1e-8)
            poses = torch.cat([t, q], dim=-1)
        return {"part_logits": logits, "part_probs": probs, "poses": poses, "attn": attn}
