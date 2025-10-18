from __future__ import annotations

from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from src.inference.edge_inference import EdgeInference


class GraspCandidate(BaseModel):
    pose: List[float]
    score: float


app = FastAPI(title="Manipulation Service")
engine = EdgeInference(pose_mode="se3")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/plan", response_model=List[GraspCandidate])
def plan(image: List[float]):
    # Expect flattened float32 RGBCHW 1x3x224x224
    arr = np.array(image, dtype=np.float32).reshape(1, 3, 224, 224)
    out = engine.infer_numpy(arr)
    poses = out["poses"][0]  # (num_parts, 7)
    probs = out["part_probs"][0]
    cands: List[GraspCandidate] = []
    for i in range(min(len(poses), 5)):
        cands.append(GraspCandidate(pose=poses[i].tolist(), score=float(probs[i])))
    cands.sort(key=lambda x: x.score, reverse=True)
    return cands
