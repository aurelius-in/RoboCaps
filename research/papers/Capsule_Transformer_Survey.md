# Capsules and Transformers for Structured Vision: A Survey

Affiliation: Boston University, M.S. Program (2018)
Advisor: Prof. Eric Braude

## Abstract
We review capsule networks and transformer-based vision backbones through the lens of structured perception: part–whole composition, pose representation, and equivariance. We synthesize results from capsules (routing, generative variants), equivariant architectures, and modern attention models to argue for capsule-style heads as structured decoders atop transformers. We emphasize robotics applications where pose-aware and interpretable outputs are essential.

## 1. Introduction
Capsules encode parts and their poses, while transformers excel at global context. We ask: when and how should capsules be used on top of attention backbones? We present a taxonomy spanning routing mechanisms, pose parameterizations, and training objectives.

## 2. Capsule Networks
- Dynamic routing and EM routing [1,2]
- Generative capsule models and autoencoders [7]
- Agreement as a principle: composition and robustness to occlusion
- Training challenges: stability, scaling, and hyperparameters

## 3. Equivariance Foundations
- Group equivariant CNNs and steerable filters [3,4]
- Tensor field networks, SE(3)-Transformers, and EGNNs [5,8,9]
- Losses and evaluation: equivariance error, canonicalization accuracy

## 4. Transformers for Vision
- ViT and hierarchical variants [10]
- Detection and segmentation heads; attention as soft routing
- Feature tokens as child votes feeding structured heads (capsules)

## 5. Routing as Attention
- Mapping agreement to attention scores with parent queries and child keys/values
- Benefits: kernel availability, stability, integration with ViT/ConvNeXt
- Trade-offs: number of parents, head dimension, and interpretability

## 6. Pose Parameterizations
- SE(2): translation and in-plane rotation for planar tasks
- SE(3): translation and quaternion rotation for 6D poses
- Regularization: unit-quaternion constraints, pose-consistency losses

## 7. Robotics-Relevant Tasks
- Industrial QA: part verification, pose-grounded defect reasoning; need for auditability
- Manipulation: affordances from structured part–pose; trajectory planning interfaces
- Sim2Real: domain randomization and evaluation loops; capsule pose stability aids transfer

## 8. Empirical Themes (2018–2024)
- Capsules show improved part-level robustness under occlusion and clutter in small-to-midscale studies; transformers supply strong features; hybrids excel when pose is central.
- Equivariance-aware training reduces sample complexity for pose estimation.
- Edge deployment is practical with ONNX/ORT/TRT and attention kernels.

## 9. Open Problems
- Adaptive parent cardinality and object grouping
- Joint learning of part taxonomies and control affordances
- Large-scale benchmarks for capsule heads atop transformers

## 10. Recommendations
Use capsule-style heads when tasks demand explicit part–pose reasoning, interpretability, and robustness to viewpoint/lighting changes—especially in robotics and QA.

## References
[1] Sabour et al., Dynamic Routing Between Capsules. NeurIPS 2017.
[2] Hinton et al., Matrix Capsules with EM Routing. ICLR 2018.
[3] Cohen & Welling, Group Equivariant CNNs. ICML 2016.
[4] Worrall et al., Harmonic Networks. CVPR 2017.
[5] Thomas et al., Tensor Field Networks. NeurIPS 2018.
[7] Kosiorek et al., Stacked Capsule Autoencoders. NeurIPS 2019.
[8] Fuchs et al., SE(3)-Transformers. NeurIPS 2020.
[9] Satorras et al., EGNN. ICML 2021.
[10] Dosovitskiy et al., ViT. ICLR 2021.

## Acknowledgments
Prepared during the author’s Master of Science studies at Boston University (2018) under Prof. Eric Braude.
