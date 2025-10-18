from __future__ import annotations

import argparse
from typing import Tuple

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader

from src.core.capsule_head import AttentionRoutedCapsuleHead
from src.core.pose_loss import PoseLoss
from src.training.dataloader import build_dataloader
from src.utils.backbones import get_backbone
from src.utils.logging import get_logger


def build_model(num_parts: int = 8, backbone_kind: str = "convnext", backbone_name: str = "convnext_tiny") -> Tuple[nn.Module, AttentionRoutedCapsuleHead]:
    backbone, feat_dim, forward_tokens = get_backbone(backbone_kind, backbone_name, pretrained=False)

    class TokenEncoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = backbone

        def forward(self, images: torch.Tensor) -> torch.Tensor:
            out = forward_tokens(images)
            # Drop CLS if present (ViT); keep spatial tokens
            tokens = out.features[:, 1:, :] if out.features.shape[1] > 100 else out.features
            return tokens

    encoder = TokenEncoder()
    head = AttentionRoutedCapsuleHead(input_dim=feat_dim, num_children=196, num_parts=num_parts)
    model = nn.Module()
    model.encoder = encoder  # type: ignore[attr-defined]
    model.head = head  # type: ignore[attr-defined]
    return model, head


def train_one_epoch(model: nn.Module, head: AttentionRoutedCapsuleHead, loader: DataLoader, device: torch.device, optimizer: AdamW, loss_fn: PoseLoss, logger) -> float:
    model.train()
    total = 0.0
    for batch in loader:
        images = batch["images"].to(device)
        labels = batch["part_labels"].to(device)
        poses = batch["poses"].to(device)
        optimizer.zero_grad(set_to_none=True)
        tokens = model.encoder(images)
        outputs = head(tokens)
        loss_dict = loss_fn(outputs, {"part_labels": labels, "poses": poses})
        loss = loss_dict["loss"]
        loss.backward()
        optimizer.step()
        total += float(loss.item())
    avg = total / max(1, len(loader))
    logger.info(f"train_loss={avg:.4f}")
    return avg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--num_parts", type=int, default=8)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    logger = get_logger("trainer")
    device = torch.device(args.device)
    loader = build_dataloader(batch_size=args.batch_size, num_parts=args.num_parts)
    model, head = build_model(num_parts=args.num_parts)
    model.to(device)
    head.to(device)

    optimizer = AdamW(head.parameters(), lr=3e-4)
    loss_fn = PoseLoss()

    for epoch in range(args.epochs):
        train_one_epoch(model, head, loader, device, optimizer, loss_fn, logger)

    logger.info("Training complete")


if __name__ == "__main__":
    main()
