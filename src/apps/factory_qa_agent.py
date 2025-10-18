from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from src.inference.edge_inference import EdgeInference
from src.utils.config import FactoryQAAgentSettings, load_yaml
from src.visualization.audit_trail_export import export_jsonl
from src.visualization.explainability_overlay import draw_capsules


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/factory_qa_agent.yaml")
    args = parser.parse_args()

    cfg_dict = load_yaml(args.config)
    settings = FactoryQAAgentSettings(**cfg_dict.get("factory_qa_agent", {}))

    edge = EdgeInference(pose_mode="se2")
    input_dir = Path(settings.input_dir)
    overlay_dir = Path(settings.overlay_dir)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    for img_path in sorted(input_dir.glob("*.jpg")):
        img_bgr = cv2.imread(str(img_path))
        if img_bgr is None:
            continue
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, settings.resize_hw[::-1])
        tensor = (img_resized.astype(np.float32) / 255.0).transpose(2, 0, 1)[None, ...]
        out = edge.infer_numpy(tensor)
        probs = out["part_probs"][0]
        poses = out["poses"][0]
        overlay = draw_capsules(img_bgr, poses, probs)
        out_path = overlay_dir / f"{img_path.stem}_overlay.jpg"
        cv2.imwrite(str(out_path), overlay)
        export_jsonl(
            settings.audit_path,
            {
                "image": str(img_path),
                "overlay": str(out_path),
                "part_probs": probs.tolist(),
                "poses": poses.tolist(),
            },
        )


if __name__ == "__main__":
    main()
