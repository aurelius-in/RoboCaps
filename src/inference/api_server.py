from __future__ import annotations

import io
from typing import Dict

import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from src.inference.edge_inference import EdgeInference


class InferResponse(BaseModel):
    part_probs: list[list[float]]
    poses: list[list[list[float]]]


app = FastAPI(title="RoboCaps API")
engine = EdgeInference()


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/infer", response_model=InferResponse)
async def infer(file: UploadFile = File(...)) -> InferResponse:
    raw = await file.read()
    # Expect raw float32 tensor serialized as CHW 224x224, single image
    arr = np.frombuffer(raw, dtype=np.float32).reshape(1, 3, 224, 224)
    out = engine.infer_numpy(arr)
    return InferResponse(part_probs=out["part_probs"].tolist(), poses=out["poses"].tolist())


@app.get("/metrics")
def metrics() -> str:
    return "# HELP robocaps_dummy 1\n# TYPE robocaps_dummy counter\nrobocaps_dummy 1\n"
