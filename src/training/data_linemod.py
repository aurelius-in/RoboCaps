from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


@dataclass
class LinemodSample:
    image: torch.Tensor  # (3,H,W)
    mask: torch.Tensor  # (1,H,W)
    poses_se3: torch.Tensor  # (num_objects, 7) as (tx,ty,tz,qw,qx,qy,qz)
    intrinsics: torch.Tensor  # (3,3)


class LineMODDataset(Dataset[LinemodSample]):
    def __init__(self, root: str | Path, split: str = "train", image_size: Tuple[int, int] = (480, 640)) -> None:
        self.root = Path(root)
        self.split = split
        self.image_size = image_size
        idx_file = self.root / f"{split}.json"
        if not idx_file.exists():
            raise FileNotFoundError(f"Missing index file: {idx_file}")
        with idx_file.open("r", encoding="utf-8") as f:
            self.index = json.load(f)
        if not isinstance(self.index, list) or len(self.index) == 0:
            raise ValueError("Index must be a non-empty list")

    def __len__(self) -> int:
        return len(self.index)

    def _load_image(self, path: Path) -> torch.Tensor:
        # Placeholder loader: replace with cv2.imread or PIL
        h, w = self.image_size
        return torch.rand(3, h, w)

    def _load_mask(self, path: Path) -> torch.Tensor:
        h, w = self.image_size
        return torch.rand(1, h, w)

    def _load_intrinsics(self, path: Path) -> torch.Tensor:
        K = torch.eye(3)
        return K

    def __getitem__(self, idx: int) -> LinemodSample:
        item = self.index[idx]
        img_path = self.root / item["image"]
        mask_path = self.root / item.get("mask", "") if item.get("mask") else None
        pose_list: List[List[float]] = item.get("poses", [])
        intr_path = self.root / item.get("intrinsics", "") if item.get("intrinsics") else None

        image = self._load_image(img_path)
        mask = self._load_mask(mask_path) if mask_path else torch.zeros(1, *self.image_size)
        poses = torch.tensor(pose_list, dtype=torch.float32) if pose_list else torch.zeros(1, 7)
        intr = self._load_intrinsics(intr_path) if intr_path else torch.eye(3)
        return LinemodSample(image=image, mask=mask, poses_se3=poses, intrinsics=intr)


def collate_fn(batch: list[LinemodSample]) -> Dict[str, torch.Tensor]:
    images = torch.stack([b.image for b in batch], 0)
    masks = torch.stack([b.mask for b in batch], 0)
    intr = torch.stack([b.intrinsics for b in batch], 0)
    # Pad variable number of objects to max in batch
    max_n = max(b.poses_se3.shape[0] for b in batch)
    poses = torch.zeros(len(batch), max_n, 7)
    for i, b in enumerate(batch):
        n = b.poses_se3.shape[0]
        poses[i, :n] = b.poses_se3
    return {"images": images, "masks": masks, "poses_se3": poses, "intrinsics": intr}


def build_linemod_loader(root: str | Path, split: str = "train", batch_size: int = 4) -> DataLoader:
    ds = LineMODDataset(root=root, split=split)
    return DataLoader(ds, batch_size=batch_size, shuffle=(split == "train"), num_workers=0, collate_fn=collate_fn)
