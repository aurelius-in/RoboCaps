<!-- b5159508-8b4a-4479-892f-2c0604563228 ac2b2984-613a-49cb-b418-84255f549989 -->
# RoboCaps Phase 2: Benchmarking & Hardening

## Scope and Defaults
- Benchmarks: LineMOD (+ Occlusion) primary; YCB-Video as secondary
- Edge target: Jetson Orin (FP16/INT8), x86+RTX validated
- Outcomes: reproducible benchmarks, optimized edge inference, deployment maturity

## 1) Benchmark Datasets & Loaders
- Add dataset loaders and configs:
  - `src/training/data_linemod.py` (images, masks, 6D poses, intrinsics)
  - `research/datasets/linemod/README.md` (structure, licensing)
- Config templates under `configs/linemod.yaml` (paths, intrinsics, objects)
- Data integrity checks (hash, count, split) in loader init

## 2) Metrics & Evaluation
- Implement ADD/ADD-S, 2D reprojection error, and pose AUC:
  - `src/utils/metrics.py` with SE(3) utilities
  - `src/training/eval_bench.py` CLI: evaluate a checkpoint across test split
- Log to `research/experiments/results/linemod/*.jsonl` and aggregate CSV

## 3) Model Improvements (SE(3) & Training)
- Extend capsule head to optional SE(3) pose (tx, ty, tz, qw, qx, qy, qz)
- Curriculum: start SE(2) → unlock depth/rotation once stable
- Training upgrades: cosine scheduler, EMA weights, mixed precision, checkpoint-best-by-metric

## 4) Edge Inference Optimization
- ONNX export enhancements: dynamic shapes, opset locking, numerical parity test
- TensorRT: build FP16 engine; optional INT8 with simple image calibration
- Throughput/latency harness: warmup, batching, FPS/latency percentiles

## 5) Deployment Maturity
- Helm chart: `deployment/k8s/helm/robocaps` (values for GPU resources, image, env)
- Registry publish: GHCR `ghcr.io/<org>/robocaps-api`
- Observability: Prometheus metrics for inference time and errors

## 6) Testing & QA
- Unit tests: routing attention shapes, loss numerics, metrics correctness
- Golden tests for ONNX parity on fixed seeds
- Smoke e2e: start API, run one infer, verify schema

## 7) Documentation & Artifacts
- `docs/academic/benchmarking.md`: protocol, metrics, seeds
- `docs/corporate/case_study_factory_qa.md`: ROI framing with hypothetical numbers
- Update `README.md` quickstart for dataset setup and benchmarking

## Milestones
- M1: LineMOD loader + metrics working (1 week)
- M2: SE(3) model + training stable (1 week)
- M3: TRT FP16 engine with throughput targets on Orin (0.5 week)
- M4: Helm deploy + GHCR publish + docs (0.5 week)

## Key Files To Be Added
- `src/training/data_linemod.py`, `src/training/eval_bench.py`
- `src/utils/metrics.py` (SE(3) utils, ADD/ADD-S)
- `configs/linemod.yaml`, `research/datasets/linemod/README.md`
- `deployment/k8s/helm/robocaps/**`
- CI additions for GHCR push


### To-dos

- [x] Implement LineMOD dataset loader and config templates
- [x] Add ADD/ADD-S and eval CLI; log benchmark outputs
- [x] Extend capsule head to optional SE(3) pose output
- [x] Build FP16/INT8 TRT engines and perf harness
- [x] Create Helm chart for API with GPU values
- [x] Publish images to GHCR via CI updates
- [x] Add unit/golden/e2e smoke tests
- [x] Add benchmarking and case study docs; update README
