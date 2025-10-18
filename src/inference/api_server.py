from __future__ import annotations

import io
import time
from typing import Dict, List

import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist

from src.inference.edge_inference import EdgeInference

try:
    from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
except Exception:  # pragma: no cover
    Histogram = None  # type: ignore
    generate_latest = None  # type: ignore
    CONTENT_TYPE_LATEST = "text/plain"  # type: ignore


class InferResponse(BaseModel):
    part_probs: List[List[float]]
    poses: List[List[List[float]]]


class InferArrayRequest(BaseModel):
    # Flattened float32 array of shape (B,3,224,224)
    array: conlist(float, min_items=1)
    batch: int = 1


app = FastAPI(title="RoboCaps API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = EdgeInference()

latency_hist = (
    Histogram("robocaps_infer_latency_ms", "Inference latency in milliseconds") if Histogram else None
)


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/infer", response_model=InferResponse)
async def infer(file: UploadFile = File(...)) -> InferResponse:
    raw = await file.read()
    # Expect raw float32 tensor serialized as CHW 224x224, single image
    arr = np.frombuffer(raw, dtype=np.float32).reshape(1, 3, 224, 224)
    t0 = time.time()
    out = engine.infer_numpy(arr)
    if latency_hist:
        latency_hist.observe((time.time() - t0) * 1000.0)
    return InferResponse(part_probs=out["part_probs"].tolist(), poses=out["poses"].tolist())


@app.post("/infer-image", response_model=InferResponse)
async def infer_image(file: UploadFile = File(...)) -> InferResponse:
    # Accept standard image bytes (e.g., JPEG/PNG)
    data = await file.read()
    buf = np.frombuffer(data, dtype=np.uint8)
    # Lazy import to avoid hard dep
    import cv2  # type: ignore

    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    arr = (img.astype(np.float32) / 255.0).transpose(2, 0, 1)[None, ...]
    t0 = time.time()
    out = engine.infer_numpy(arr)
    if latency_hist:
        latency_hist.observe((time.time() - t0) * 1000.0)
    return InferResponse(part_probs=out["part_probs"].tolist(), poses=out["poses"].tolist())


@app.post("/infer-array", response_model=InferResponse)
async def infer_array(req: InferArrayRequest) -> InferResponse:
    arr = np.array(req.array, dtype=np.float32).reshape(req.batch, 3, 224, 224)
    t0 = time.time()
    out = engine.infer_numpy(arr)
    if latency_hist:
        latency_hist.observe((time.time() - t0) * 1000.0)
    return InferResponse(part_probs=out["part_probs"].tolist(), poses=out["poses"].tolist())


@app.get("/metrics")
def metrics():
    if generate_latest:
        body = generate_latest()  # type: ignore
        return app.response_class(content=body, media_type=CONTENT_TYPE_LATEST)  # type: ignore
    return "# robocaps metrics disabled\n"
