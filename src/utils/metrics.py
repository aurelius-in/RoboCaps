from __future__ import annotations

import math
from typing import Tuple

import torch


def quat_to_rotmat(q: torch.Tensor) -> torch.Tensor:
    """Convert quaternion (w,x,y,z) to rotation matrix.
    q: (..., 4)
    returns: (..., 3, 3)
    """
    qw, qx, qy, qz = q.unbind(-1)
    xx = qx * qx
    yy = qy * qy
    zz = qz * qz
    xy = qx * qy
    xz = qx * qz
    yz = qy * qz
    wx = qw * qx
    wy = qw * qy
    wz = qw * qz
    R = torch.stack(
        [
            1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy),
            2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx),
            2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy),
        ],
        dim=-1,
    ).reshape(q.shape[:-1] + (3, 3))
    return R


def se3_to_mat(tx_ty_tz_qw_qx_qy_qz: torch.Tensor) -> torch.Tensor:
    t = tx_ty_tz_qw_qx_qy_qz[..., :3]
    q = tx_ty_tz_qw_qx_qy_qz[..., 3:]
    R = quat_to_rotmat(q / (q.norm(dim=-1, keepdim=True) + 1e-8))
    T = torch.eye(4, device=tx_ty_tz_qw_qx_qy_qz.device).repeat(tx_ty_tz_qw_qx_qy_qz.shape[0], 1, 1)
    T[:, :3, :3] = R
    T[:, :3, 3] = t
    return T


def add_metric(pred_pts: torch.Tensor, gt_pts: torch.Tensor) -> torch.Tensor:
    """Average distance of model points (ADD). Both are (N,3)."""
    return (pred_pts - gt_pts).norm(dim=-1).mean()


def add_s_metric(pred_pts: torch.Tensor, gt_pts: torch.Tensor) -> torch.Tensor:
    """Symmetric ADD-S: mean over nearest neighbor distances.
    For simplicity, use pairwise distances; optimized version can use k-d tree.
    """
    dists = torch.cdist(pred_pts, gt_pts)
    nn = dists.min(dim=-1).values
    return nn.mean()
