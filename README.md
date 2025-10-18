# RoboCaps

Structured Part–Pose Capsules for Robotic Perception

## Why this repository exists
Modern robotic perception often relies on detectors that output flat labels and boxes. That is sufficient for coarse scene understanding, but insufficient when robots must reason about parts, poses, topology, occlusion, and actionability under tight latency budgets. Capsule Networks were introduced to explicitly model part–whole relationships and poses, yet they remain underutilized in production perception systems despite their fit to robotics. RoboCaps reintroduces capsules with a practical, high-performance implementation that integrates attention-based routing, transformer/ConvNeXt backbones, and edge deployment.

In robotics, perception outputs should be structured and actionable: part identities, calibrated confidences, and SE(2)/SE(3) poses, all traceable and auditable. Capsules are uniquely suited to this, because they:
- encode part–whole composition and agreement, not just presence [1,2]
- represent pose as a first-class quantity rather than an afterthought [1,2]
- enable equivariance-aware objectives that improve stability under viewpoint/lighting changes [3–6]
- naturally yield interpretable attention/routing maps for explainability and QA

RoboCaps operationalizes these properties for three real-world systems: Factory QA, Robot Manipulation, and Sim2Real.

## Apps (ready to run)
- Factory QA Edge Agent (CLI):
  - Config: `configs/factory_qa_agent.yaml`
  - Run: `python -m src.apps.factory_qa_agent --config configs/factory_qa_agent.yaml`
- Manipulation Service (FastAPI):
  - Run: `uvicorn src.apps.manipulation_service:app --host 0.0.0.0 --port 8001`
- Sim2Real Orchestrator (CLI):
  - Config: `configs/sim2real.yaml`
  - Run: `python -m src.apps.sim2real_orchestrator --config configs/sim2real.yaml`

Docker Compose: `docker compose -f deployment/docker/compose.yaml up --build`

Kubernetes: apply manifests in `deployment/k8s/`.

## Structure
```
.
├── research/                # Papers, experiments, datasets
├── architecture/            # Architecture docs & diagrams
├── src/                     # Core library, apps, training, inference, viz
├── deployment/              # Docker, K8s, edge systemd, CI/CD guides
├── docs/                    # Academic, corporate, marketing, product, roadmap
└── pitch/                   # Whitepaper, investor deck, vision
```

## What makes RoboCaps different
- Attention-routed capsules: we cast routing-by-agreement as multi-head attention to stabilize training and leverage mature GPU kernels, while preserving the core agreement principle [1,2].
- Pose-first heads: SE(2) and SE(3) parameterizations are native outputs; pose losses include consistency and equivariance regularization [3–6].
- Plug-and-play backbones: ViT/ConvNeXt adapters provide tokens or feature maps; capsules act as structured heads on top.
- Edge-grade inference: ONNX export + TensorRT (FP16/INT8) delivers low-latency, audit-ready inference on Jetson/x86 GPUs.
- Explainability and auditability: pose overlays, routing attention, and JSONL audit trails built-in.
- Production architecture: C4/RM-ODP docs, high-contrast Mermaid diagrams, Docker/K8s/Helm, CI/CD (lint, tests, SBOM, GHCR images).

## Why Capsules for robotics (and why now)
Capsules explicitly model part–whole structure and poses. For robots, this yields tangible advantages:
- Robustness via structure: agreement between parts and wholes mitigates spurious detections under clutter or partial occlusion [1,2].
- Pose equivariance: objectives that respect SE(2)/SE(3) structure reduce data demand for viewpoint generalization [3–6].
- Action readiness: poses and part confidences map directly to control frames and grasp/QA decisions.
- Interpretability: routing/attention weights and pose vectors provide human-auditable rationales—critical for QA and HRI.
- Edge efficiency: attention routing is kernel-friendly and amenable to quantization; structured heads minimize post-processing.

The timing is right because: transformer backbones are ubiquitous; ONNX/TRT make deployment routine; enterprises require explainable, auditable perception; and robotics workloads increasingly demand structured outputs.

## Systems in this repo
- Factory QA (System A): inline defect detection, part verification, pose-grounded audit. Edge-first with ROS2/MQTT integration.
- Robot Manipulation (System B): part/pose perception → affordances → planning. Wrist/overhead cameras, MoveIt integration.
- Sim2Real (System C): domain randomization, evaluation, and adaptation loops to shrink the sim-to-real gap.

See `architecture/` for detailed C4/RM-ODP docs and high-contrast diagrams.

## Technical overview
- `src/core/`: `RoutingAttention` and `AttentionRoutedCapsuleHead` produce part confidences and poses (SE(2)/SE(3)).
- `src/utils/backbones.py`: ViT/ConvNeXt adapters yielding tokens/features.
- `src/training/`: PyTorch training, synthetic dataset, benchmarking CLI.
- `src/inference/`: ONNX export, TensorRT/ORT runtime, FastAPI server.
- `src/visualization/`: pose overlays and audit export tools.

## Expected benefits (by design)
- Accuracy and stability: pose-aware heads and equivariance regularization can improve part AP and reduce pose error, especially under viewpoint/lighting shifts [3–6].
- Efficiency: attention-based routing is parallelizable; with TensorRT FP16/INT8, sub-60 ms p50 on Jetson-class devices is an attainable target for typical 224×224 inputs (workload-dependent).
- Explainability: interpretable routing maps and pose vectors enable operator trust and faster root-cause analysis in QA lines.

## Quickstart
1. Create a Python 3.10 environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run API server: `uvicorn src.inference.api_server:app --reload`

## Datasets & Benchmarking
- LineMOD structure documented in `research/datasets/linemod/README.md`
- Config template: `configs/linemod.yaml`
- Evaluate (placeholder): `python -m src.training.eval_bench --data_root research/datasets/linemod`

## Roadmap
- SE(3) training recipes and public benchmarks
- INT8 calibration notebooks and calibration artifact formats
- Multi-vertical adapters (QA, manipulation, logistics), SDKs, and managed deployment profiles

## References
```
[1] Sabour, Frosst, Hinton. Dynamic Routing Between Capsules. NeurIPS 2017.
[2] Hinton, Sabour, Frosst. Matrix Capsules with EM Routing. ICLR 2018.
[3] Cohen, Welling. Group Equivariant Convolutional Networks. ICML 2016.
[4] Worrall et al. Harmonic Networks: Deep Translation and Rotation Equivariance. CVPR 2017.
[5] Thomas et al. Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks. arXiv 2018.
[6] Kondor, Trivedi. On the Generalization of Equivariance and Convolution in Neural Networks to the Action of Compact Groups. ICML 2018.
[7] Dosovitskiy et al. An Image is Worth 16×16 Words: Transformers for Image Recognition at Scale. ICLR 2021.
```
—
For high-level product/market framing, see `docs/marketing/` and `pitch/`. For deployment, see `deployment/` and the Helm chart in `deployment/k8s/helm/robocaps`.
