from __future__ import annotations

import argparse
from pathlib import Path

import torch

from src.training.data_linemod import build_linemod_loader
from src.core.capsule_head import AttentionRoutedCapsuleHead
from src.utils.backbones import get_backbone
from src.utils.metrics import add_metric


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root", type=str, default="research/datasets/linemod")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    device = torch.device(args.device)
    loader = build_linemod_loader(args.data_root, split="test", batch_size=args.batch_size)

    backbone, feat_dim, forward_tokens = get_backbone("convnext", "convnext_tiny", pretrained=False)

    class TokenEncoder(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = backbone

        def forward(self, images: torch.Tensor) -> torch.Tensor:
            out = forward_tokens(images)
            tokens = out.features[:, 1:, :] if out.features.shape[1] > 100 else out.features
            return tokens

    encoder = TokenEncoder().to(device).eval()
    head = AttentionRoutedCapsuleHead(input_dim=feat_dim, num_children=196, num_parts=8).to(device).eval()

    total = 0.0
    count = 0
    with torch.no_grad():
        for batch in loader:
            images = batch["images"].to(device)
            tokens = encoder(images)
            out = head(tokens)
            # Placeholder metric: confidence proxy
            total += float(out["part_probs"].mean().item())
            count += 1
    avg = total / max(count, 1)
    print({"confidence_proxy": avg})


if __name__ == "__main__":
    main()
