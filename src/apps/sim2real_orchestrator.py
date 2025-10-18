from __future__ import annotations

import argparse
import random
from pathlib import Path

from src.utils.config import Sim2RealSettings, load_yaml
from src.visualization.audit_trail_export import export_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/sim2real.yaml")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    settings = Sim2RealSettings(**cfg.get("sim2real", {}))

    out_path = Path(settings.results_path)
    for i in range(settings.runs):
        seed = settings.seeds[i % len(settings.seeds)] if settings.seeds else i
        random.seed(seed)
        # Placeholder: emulate a run with synthetic metrics
        metrics = {
            "seed": seed,
            "add_s": round(random.uniform(0.75, 0.9), 3),
            "pose_l1": round(random.uniform(0.03, 0.08), 3),
            "equivariance_error": round(random.uniform(0.01, 0.04), 3),
        }
        export_jsonl(out_path, metrics)
    print(f"Wrote results to {out_path}")


if __name__ == "__main__":
    main()
