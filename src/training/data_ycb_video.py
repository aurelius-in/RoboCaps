from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

import torch
from torch.utils.data import Dataset, DataLoader


@dataclass
class YCBVideoSample:
    image: torch.Tensor  # (3,H,W)
    poses_se3: torch.Tensor  # (num_objects, 7)
    intrinsics: torch.Tensor  # (3,3)


class YCBVideoDataset(Dataset[YCBVideoSample]):
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
        h, w = self.image_size
        return torch.rand(3, h, w)

    def _load_intrinsics(self, K_path: Path) -> torch.Tensor:
        if K_path.exists():
            with K_path.open("r", encoding="utf-8") as f:
                vals = [float(x) for x in f.read().split()]
            if len(vals) >= 9:
                K = torch.tensor(vals[:9], dtype=torch.float32).reshape(3, 3)
                return K
        return torch.eye(3)

    def __getitem__(self, idx: int) -> YCBVideoSample:
        item = self.index[idx]
        img_path = self.root / item["image"]
        K_path = self.root / item.get("intrinsics", "") if item.get("intrinsics") else None
        poses = torch.tensor(item.get("poses", []), dtype=torch.float32) if item.get("poses") else torch.zeros(1, 7)
        image = self._load_image(img_path)
        K = self._load_intrinsics(K_path) if K_path else torch.eye(3)
        return YCBVideoSample(image=image, poses_se3=poses, intrinsics=K)


def collate_fn(batch: list[YCBVideoSample]) -> Dict[str, torch.Tensor]:
    images = torch.stack([b.image for b in batch], 0)
    intr = torch.stack([b.intrinsics for b in batch], 0)
    max_n = max(b.poses_se3.shape[0] for b in batch)
    poses = torch.zeros(len(batch), max_n, 7)
    for i, b in enumerate(batch):
        n = b.poses_se3.shape[0]
        poses[i, :n] = b.poses_se3
    return {"images": images, "intrinsics": intr, "poses_se3": poses}


def build_ycb_loader(root: str | Path, split: str = "train", batch_size: int = 4) -> DataLoader:
    ds = YCBVideoDataset(root=root, split=split)
    return DataLoader(ds, batch_size=batch_size, shuffle=(split == "train"), num_workers=0, collate_fn=collate_fn)
