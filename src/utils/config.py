from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class FactoryQAAgentSettings(BaseModel):
    input_dir: str = Field(default="data/input")
    overlay_dir: str = Field(default="data/overlays")
    audit_path: str = Field(default="data/audit/qa.jsonl")
    batch_size: int = Field(default=1)
    resize_hw: tuple[int, int] = Field(default=(224, 224))
    api_url: Optional[str] = Field(default=None, description="Optional API to POST results")


class ManipServiceSettings(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8001)
    resize_hw: tuple[int, int] = Field(default=(224, 224))


class Sim2RealSettings(BaseModel):
    results_path: str = Field(default="research/experiments/results/sim2real.jsonl")
    runs: int = Field(default=5)
    seeds: list[int] = Field(default_factory=lambda: [1, 2, 3])


def load_yaml(path: str | Path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
