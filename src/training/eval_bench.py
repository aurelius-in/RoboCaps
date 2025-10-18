from __future__ import annotations

import argparse
import csv
from pathlib import Path

import torch

from src.training.data_linemod import build_linemod_loader
from src.training.data_ycb_video import build_ycb_loader
from src.core.capsule_head import AttentionRoutedCapsuleHead
from src.utils.backbones import get_backbone


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=["linemod", "ycb"], default="linemod")
    parser.add_argument("--data_root", type=str, default="research/datasets/linemod")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--out_csv", type=str, default="research/experiments/results/bench.csv")
    args = parser.parse_args()

    device = torch.device(args.device)
    if args.dataset == "linemod":
        loader = build_linemod_loader(args.data_root, split="test", batch_size=args.batch_size)
    else:
        loader = build_ycb_loader(args.data_root, split="test", batch_size=args.batch_size)

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

    rows = []
    with torch.no_grad():
        for batch in loader:
            images = batch["images"].to(device)
            tokens = encoder(images)
            out = head(tokens)
            rows.append({
                "confidence_proxy": float(out["part_probs"].mean().item()),
                "num_parts": out["part_probs"].shape[1],
            })
    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
