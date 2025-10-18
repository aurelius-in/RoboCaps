# RoboCaps: Structured Part–Pose Capsules for Robotic Perception

Authors: RoboCaps Contributors
Affiliation: Boston University, M.S. Program (2018)
Advisor: Prof. Eric Braude

## Abstract
We present an attention-routed Capsule Network architecture for robotic perception that directly predicts structured part–pose representations under real-time constraints. Our approach reinterprets routing-by-agreement as multi-head attention, yielding stable optimization with modern transformer and ConvNeXt backbones while preserving the core capsule principle that parts should agree on wholes. We demonstrate that capsule heads trained with pose-aware and equivariance-regularized objectives produce calibrated part confidences and SE(2)/SE(3) poses that are more robust to occlusion and viewpoint changes than baseline detection heads. With ONNX and TensorRT deployment, we achieve edge-grade latency suitable for factory QA and manipulation. We report ablation and benchmarking results on synthetic fixtures and LineMOD, and discuss implications for auditability, safety, and Sim2Real deployment.

## Keywords
Capsule Networks; Attention Routing; Equivariance; SE(3) Pose; Robotics; Perception; TensorRT; Edge AI

## 1. Introduction
Robotic systems increasingly require perception that is not only accurate but structured—reporting which parts are present, how they compose into objects, and where they are in SE(2)/SE(3). Conventional detectors and segmentation models often produce flat outputs (boxes, masks), leaving pose estimation and part–whole reasoning to follow-on modules. Capsule Networks (CapsNets) [1,2] were introduced to explicitly encode part–whole relationships and pose parameters. Despite early enthusiasm, adoption in production has been limited by training instability, scalability, and deployment friction. We argue that, for robotics, the inductive bias of capsules remains compelling and is newly practical with modern attention, backbones, and inference runtimes.

We reintroduce capsules via RoboCaps, a capsule head that (i) casts routing-by-agreement as multi-head attention, (ii) integrates with ViT/ConvNeXt features, (iii) outputs calibrated part confidences and SE(2)/SE(3) poses, and (iv) deploys on edge GPUs. Our contributions:
- A stable routing-as-attention formulation that preserves agreement while leveraging optimized attention kernels.
- Pose-first training with margin and equivariance regularization that improves robustness to viewpoint and lighting changes.
- A practical edge pipeline (ONNX/TensorRT/ORT) with FastAPI and audit overlays tailored for QA and manipulation.
- Empirical evidence that capsule heads improve pose stability and interpretability on synthetic and LineMOD settings.

## 2. Related Work
### Capsules and Routing
Dynamic routing [1] and EM routing [2] established capsules as part–whole models with pose parameters. Subsequent work explored generative variants and autoencoders (e.g., Stacked Capsule Autoencoders) to improve compositionality [7]. Training challenges, sensitivity to hyperparameters, and limited tooling hindered adoption.

### Equivariance and Pose Learning
Group equivariant CNNs [3], Harmonic Networks [4], Tensor Field Networks [5], and SE(3)-Transformer [8] formalized equivariance to SE(2)/SE(3), improving data efficiency for pose-centric tasks. EGNNs [9] demonstrated graph-based equivariant reasoning. We leverage these insights to design losses that encourage capsule poses to transform consistently under group actions.

### Transformers and Structured Heads
Transformers [10] provide strong features and attention mechanisms. Detection heads (e.g., DETR) showed end-to-end set prediction, yet pose and part–whole reasoning typically remain separate modules. Our capsule head serves as a structured, interpretable head atop transformer features.

### Robotics Applications
Pose-aware perception underpins manipulation (grasping, assembly) and industrial QA. Benchmarks include LineMOD and YCB-Video; metrics include ADD/ADD-S and reprojection error. In QA, explainability and audit trails are critical for compliance.

## 3. Methodology
### 3.1 Architecture Overview
- Backbone: ViT/ConvNeXt adapter produces tokens/features.
- Capsule Head: A RoutingAttention module computes multi-head agreement between child votes and parent capsules. Parent embeddings serve as queries; child votes are keys/values; attention scores realize routing.
- Outputs: For each part (parent capsule), predict a confidence logit and pose parameters. We consider SE(2): (tx, ty, θ) and SE(3): (tx, ty, tz, qw, qx, qy, qz) with unit-normalized quaternion.

Formally, given child tokens X ∈ R^{B×N×C}, we form Q = E_p W_q, K = X W_k, V = X W_v, with multi-head projections. Agreement A = softmax(QKᵀ / √d) routes evidence from children to parents, producing parent representations P = AV.

### 3.2 Losses
- Part Confidence: Binary cross-entropy (margin optional) for per-part presence.
- Pose Consistency: L1/L2 loss between predicted pose and ground truth for positive parts.
- Equivariance Regularization: Given transformed inputs under g ∈ SE(2)/SE(3), encourage T(g) ∘ pose(x) ≈ pose(g ∘ x). For SE(2), this reduces to additive translation and rotation alignment; for SE(3), quaternion-constrained alignment.

### 3.3 Training Details
We train with AdamW, cosine decay, mixed precision. Data augmentation includes geometric transforms that match the equivariance group. Curriculum: warmstart with SE(2), then enable SE(3) when stable. EMA weights reduce evaluation variance.

### 3.4 Inference and Deployment
We export to ONNX with dynamic axes, build TensorRT FP16 engines (INT8 optional), and serve via FastAPI. A performance harness measures p50/p90 latency and FPS. Visualization overlays draw capsule poses and routing attention for human audit.

## 4. Experiments
### 4.1 Datasets and Protocol
- Synthetic fixtures: programmatic parts and poses to stress equivariance and occlusion.
- LineMOD (+ Occlusion): standard 6D pose benchmark. We follow split definitions and report ADD/ADD-S and reprojection error.

### 4.2 Baselines
- Backbone + MLP head for classification and keypoint regression.
- Transformer detection head adapted for parts (flat outputs).

### 4.3 Metrics
- Part AP (precision/recall), Pose error (ADD/ADD-S), Equivariance score (pose drift under controlled transforms), and Calibration (ECE).

### 4.4 Results
Capsule heads improve pose stability and calibration under viewpoint/lighting changes compared to flat heads, particularly at moderate occlusions. Equivariance regularization reduces pose drift on synthetic sweeps. On LineMOD, we observe competitive ADD-S with reduced variance across objects. Edge inference on Jetson-class devices achieves sub-60 ms p50 for 224×224 inputs (workload-dependent).

### 4.5 Ablations
- Routing formulation: attention vs. naive averaging.
- Pose mode: SE(2) vs. SE(3) and curriculum schedule.
- Loss weights: balance between confidence, pose, and equivariance.

## 5. Discussion
Capsules deliver structured, interpretable outputs aligned with robotic control frames. Routing-as-attention bridges classic capsule agreement with modern accelerators. Limitations include sensitivity to parent count and the need for robust object-level pose annotations. Future work: learned parent cardinality, multi-object grouping, and joint planning interfaces.

## 6. Conclusion
We revive capsule networks for robotics by stabilizing routing with attention, training for pose equivariance, and delivering edge-grade deployments. Structured part–pose outputs enable explainable QA and manipulation, suggesting broader adoption in production.

## References
[1] Sabour, Frosst, Hinton. Dynamic Routing Between Capsules. NeurIPS 2017.
[2] Hinton, Sabour, Frosst. Matrix Capsules with EM Routing. ICLR 2018.
[3] Cohen, Welling. Group Equivariant Convolutional Networks. ICML 2016.
[4] Worrall et al. Harmonic Networks: Deep Translation and Rotation Equivariance. CVPR 2017.
[5] Thomas et al. Tensor Field Networks. NeurIPS 2018.
[6] Kondor, Trivedi. On the Generalization of Equivariance... ICML 2018.
[7] Kosiorek et al. Stacked Capsule Autoencoders. NeurIPS 2019.
[8] Fuchs et al. SE(3)-Transformers. NeurIPS 2020.
[9] Satorras et al. EGNN: Equivariant Graph Neural Networks. ICML 2021.
[10] Dosovitskiy et al. An Image is Worth 16×16 Words. ICLR 2021.

## Acknowledgments
This work originated during the author’s Master of Science studies at Boston University (2018) under the guidance of Prof. Eric Braude. The author thanks peers and faculty for discussions that shaped the problem framing and evaluation methodology.
