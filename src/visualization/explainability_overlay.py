from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np


def draw_capsules(image_bgr: np.ndarray, poses: np.ndarray, confidences: np.ndarray, color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    out = image_bgr.copy()
    h, w = out.shape[:2]
    for i in range(len(poses)):
        tx, ty, theta = poses[i]
        cx = int((tx * 0.5 + 0.5) * w)
        cy = int((ty * 0.5 + 0.5) * h)
        length = int(20 + 40 * float(confidences[i]))
        dx = int(length * np.cos(theta))
        dy = int(length * np.sin(theta))
        cv2.circle(out, (cx, cy), 3, color, -1)
        cv2.arrowedLine(out, (cx, cy), (cx + dx, cy + dy), color, 2, tipLength=0.3)
    return out
