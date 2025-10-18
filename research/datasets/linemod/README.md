# LineMOD Dataset

This folder documents expected structure and licensing notes for LineMOD evaluation.

## Structure (example)
- `train.json` / `test.json`: lists of samples with fields `{image, mask, poses, intrinsics}`
- `images/`: RGB images
- `masks/`: optional binary masks
- `poses/`: per-sample 6D poses (tx,ty,tz,qw,qx,qy,qz)
- `camera_intrinsics/`: optional per-scene intrinsics

Ensure you have permission to use the dataset under its license.
