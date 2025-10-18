from __future__ import annotations

from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class RoutingAttention(nn.Module):
    """Multi-head routing-by-agreement implemented via attention.

    Inputs are child capsule votes; attention weights compute agreement with parent capsules.
    """

    def __init__(
        self,
        input_dim: int,
        num_parents: int,
        num_heads: int = 4,
        head_dim: Optional[int] = None,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        assert input_dim > 0 and num_parents > 0 and num_heads > 0
        self.input_dim = input_dim
        self.num_parents = num_parents
        self.num_heads = num_heads
        self.head_dim = head_dim or (input_dim // num_heads)
        self.scale = self.head_dim**-0.5

        proj_dim = self.num_heads * self.head_dim
        self.q_proj = nn.Linear(input_dim, proj_dim)
        self.k_proj = nn.Linear(input_dim, proj_dim)
        self.v_proj = nn.Linear(input_dim, proj_dim)
        self.out_proj = nn.Linear(proj_dim, input_dim)
        self.parent_embed = nn.Parameter(torch.randn(num_parents, input_dim) * 0.02)
        self.dropout = nn.Dropout(dropout)

    def _shape(self, x: torch.Tensor) -> torch.Tensor:
        b, n, c = x.shape
        h, d = self.num_heads, self.head_dim
        x = x.view(b, n, h, d).transpose(1, 2)  # (b, h, n, d)
        return x

    def forward(self, votes: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute routed parent representations and attention weights.

        Args:
            votes: (batch, num_children, input_dim)
        Returns:
            parents: (batch, num_parents, input_dim)
            attn_probs: (batch, num_heads, num_parents, num_children)
        """
        b, nc, c = votes.shape
        parent_queries = self.parent_embed.expand(b, self.num_parents, c)

        q = self._shape(self.q_proj(parent_queries))  # (b, h, np, d)
        k = self._shape(self.k_proj(votes))  # (b, h, nc, d)
        v = self._shape(self.v_proj(votes))  # (b, h, nc, d)

        attn_logits = torch.matmul(q, k.transpose(-2, -1)) * self.scale  # (b,h,np,nc)
        attn_probs = F.softmax(attn_logits, dim=-1)
        attn_probs = self.dropout(attn_probs)

        context = torch.matmul(attn_probs, v)  # (b,h,np,d)
        context = context.transpose(1, 2).contiguous().view(b, self.num_parents, -1)
        parents = self.out_proj(context)  # (b,np,c)
        return parents, attn_probs
