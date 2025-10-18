from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import torch

try:
    import onnxruntime as ort
except Exception:  # pragma: no cover - optional
    ort = None  # type: ignore

from src.core.capsule_head import AttentionRoutedCapsuleHead
from src.utils.backbones import get_backbone


class EdgeInference:
    def __init__(self, num_parts: int = 8, backbone_kind: str = "convnext", backbone_name: str = "convnext_tiny", pose_mode: str = "se2") -> None:
        backbone, feat_dim, forward_tokens = get_backbone(backbone_kind, backbone_name, pretrained=False)

        class TokenEncoder(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.backbone = backbone

            def forward(self, images: torch.Tensor) -> torch.Tensor:
                out = forward_tokens(images)
                tokens = out.features[:, 1:, :] if out.features.shape[1] > 100 else out.features
                return tokens

        self.encoder = TokenEncoder().eval()
        self.head = AttentionRoutedCapsuleHead(input_dim=feat_dim, num_children=196, num_parts=num_parts, pose_mode=pose_mode).eval()
        self.session: Optional[ort.InferenceSession] = None  # type: ignore

    def export_onnx(self, output_path: str | Path, opset: int = 17) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dummy = torch.randn(1, 3, 224, 224)

        class Full(torch.nn.Module):
            def __init__(self, enc, head):
                super().__init__()
                self.enc = enc
                self.head = head

            def forward(self, x):
                toks = self.enc(x)
                out = self.head(toks)
                return out["part_probs"], out["poses"]

        model = Full(self.encoder, self.head)
        torch.onnx.export(
            model,
            dummy,
            str(output_path),
            input_names=["images"],
            output_names=["part_probs", "poses"],
            opset_version=opset,
            dynamic_axes={"images": {0: "batch"}, "part_probs": {0: "batch"}, "poses": {0: "batch"}},
        )
        return output_path

    def load_onnx(self, onnx_path: str | Path) -> None:
        if ort is None:
            raise RuntimeError("onnxruntime not available")
        providers = [
            ("TensorrtExecutionProvider", {}),
            ("CUDAExecutionProvider", {}),
            ("CPUExecutionProvider", {}),
        ]
        self.session = ort.InferenceSession(str(onnx_path), providers=[p[0] for p in providers if p[0] in ort.get_available_providers()])  # type: ignore[attr-defined]

    def infer_numpy(self, image_bchw: np.ndarray) -> Dict[str, np.ndarray]:
        if self.session is None:
            # Fallback to PyTorch eager
            with torch.no_grad():
                images = torch.from_numpy(image_bchw).float()
                tokens = self.encoder(images)
                out = self.head(tokens)
                return {
                    "part_probs": out["part_probs"].cpu().numpy(),
                    "poses": out["poses"].cpu().numpy(),
                }
        inputs = {self.session.get_inputs()[0].name: image_bchw}
        part_probs, poses = self.session.run(None, inputs)
        return {"part_probs": part_probs, "poses": poses}

    def benchmark(self, iters: int = 50, batch: int = 1) -> Dict[str, float]:
        arr = np.random.rand(batch, 3, 224, 224).astype(np.float32)
        # warmup
        for _ in range(5):
            _ = self.infer_numpy(arr)
        times = []
        for _ in range(iters):
            t0 = time.time()
            _ = self.infer_numpy(arr)
            times.append((time.time() - t0) * 1000.0)
        times.sort()
        avg = float(np.mean(times))
        p50 = times[len(times) // 2]
        p90 = times[int(len(times) * 0.9)]
        fps = 1000.0 / avg if avg > 0 else 0.0
        return {"latency_ms_avg": avg, "p50_ms": p50, "p90_ms": p90, "fps": fps}
