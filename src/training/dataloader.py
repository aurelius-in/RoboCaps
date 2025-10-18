from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import torch
from torch.utils.data import Dataset, DataLoader


@dataclass
class Sample:
    image: torch.Tensor  # (3, H, W)
    part_labels: torch.Tensor  # (num_parts,)
    poses: torch.Tensor  # (num_parts, 3)


class SyntheticCapsuleDataset(Dataset[Sample]):
    def __init__(self, num_samples: int = 256, image_size: Tuple[int, int] = (224, 224), num_parts: int = 8):
        self.num_samples = num_samples
        self.image_size = image_size
        self.num_parts = num_parts

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> Sample:  # noqa: D401
        h, w = self.image_size
        image = torch.rand(3, h, w)
        part_labels = (torch.rand(self.num_parts) > 0.5).float()
        poses = torch.randn(self.num_parts, 3) * 0.1
        return Sample(image=image, part_labels=part_labels, poses=poses)


def collate_fn(batch: list[Sample]):
    images = torch.stack([s.image for s in batch], dim=0)
    labels = torch.stack([s.part_labels for s in batch], dim=0)
    poses = torch.stack([s.poses for s in batch], dim=0)
    return {"images": images, "part_labels": labels, "poses": poses}


def build_dataloader(batch_size: int = 8, num_parts: int = 8, num_samples: int = 256, image_size: Tuple[int, int] = (224, 224)) -> DataLoader:
    ds = SyntheticCapsuleDataset(num_samples=num_samples, image_size=image_size, num_parts=num_parts)
    return DataLoader(ds, batch_size=batch_size, shuffle=True, num_workers=0, collate_fn=collate_fn)
