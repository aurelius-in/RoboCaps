# RoboCaps v0.2.0

Highlights:
- Apps: Factory QA Agent (CLI), Manipulation Service (FastAPI), Sim2Real Orchestrator (CLI)
- Capsules: SE(2)/SE(3) outputs, attention routing, pose/equivariance losses
- Inference: ONNX, ORT/TRT with INT8 calibrator; parity checks and perf harness
- Datasets/Eval: LineMOD intrinsics parsing; YCB-Video loader; CSV/JSONL outputs
- Deployment: Docker Compose, K8s manifests, Helm (API + Manip), systemd unit
- CI/CD: Lint/tests, multi-image GHCR publish, scans
- Docs: research papers, deep architecture, public-ready corporate/marketing/product, pitch

Next:
- Publish benchmark artifacts for LineMOD/YCB-Video
- Add calibrated INT8 datasets and notebooks
