# Equivariance and Pose Reasoning in Vision Models

Affiliation: Boston University, M.S. Program (2018)
Advisor: Prof. Eric Braude

## Abstract
We provide a concise but detailed treatment of equivariance for vision models with a focus on pose-aware perception. We review group actions for SE(2)/SE(3), discuss architectural choices to approximate equivariance, define practical metrics, and outline how capsule heads can exploit these properties to improve stability and interpretability in robotics.

## 1. Groups, Actions, and Representations
Let G act on input space X (images) and feature space Y via π_X and π_Y. A mapping f: X→Y is equivariant if f(π_X(g)x) = π_Y(g)f(x). For SE(2)/SE(3), π_X combines translation and rotation; π_Y often follows a representation (e.g., Wigner-D for 3D).

## 2. Architectural Approximations
- Group Equivariant CNNs: tie filters across group elements [1].
- Steerable filters and harmonic networks: encode rotation structure [2].
- Tensor Field Networks and SE(3)-Transformers: use irreps to maintain equivariance [3,4].
- Attention with relative pose encodings: approximate equivariance over compact subgroups.

## 3. Pose Parameterization and Constraints
- SE(2): (tx, ty, θ) with angle wrapping.
- SE(3): (tx, ty, tz, qw, qx, qy, qz) with unit quaternion constraint.
- Regularizers: unit-norm constraints; consistency terms under known transforms.

## 4. Metrics for Practice
- Equivariance Error: E_g = || f(π_X(g)x) − π_Y(g)f(x) || averaged over sampled g.
- Canonicalization Accuracy: distance to a canonical pose after normalization.
- Pose Error: ADD/ADD-S for 6D pose benchmarks; 2D reprojection error for SE(2).
- Stability: variance of predicted pose under nuisance perturbations.

## 5. Training Strategies
- Augment with sampled group elements g and enforce consistency losses.
- Curriculum: begin with SE(2), then unlock SE(3) rotations.
- EMA and temperature scheduling for robust agreement/attention.

## 6. Capsules and Equivariance
Capsules predict poses explicitly; routing encourages agreement across transformed views. Casting routing as attention provides stable kernels while retaining the compositional bias. Combining capsule heads with equivariance-aware losses yields improved pose stability and calibrated part confidences.

## 7. Implications for Robotics
- QA: viewpoint and lighting shifts are common; equivariance reduces false rejects.
- Manipulation: explicit SE(3) outputs align to control frames; reduced pose drift improves grasp planning.
- Sim2Real: structured pose improves transfer when domain parameters shift.

## 8. Discussion and Outlook
Bridging perfect equivariance and practical architectures remains open. Promising directions include hybrid irreps-attention models and learned canonical frames. Capsules provide a natural decoding interface for pose-aware backbones.

## References
[1] Cohen & Welling. Group Equivariant CNNs. ICML 2016.
[2] Worrall et al. Harmonic Networks. CVPR 2017.
[3] Thomas et al. Tensor Field Networks. NeurIPS 2018.
[4] Fuchs et al. SE(3)-Transformers. NeurIPS 2020.

## Acknowledgments
Created during the author’s Master of Science studies at Boston University (2018) with guidance from Prof. Eric Braude.
