from __future__ import annotations

from typing import Callable, Iterable, Optional

import numpy as np

try:
    import tensorrt as trt  # type: ignore
    import pycuda.autoinit  # type: ignore  # noqa: F401
    import pycuda.driver as cuda  # type: ignore
except Exception as e:  # pragma: no cover
    trt = None  # type: ignore
    cuda = None  # type: ignore


class NumpyEntropyCalibrator:
    """TensorRT INT8 calibrator for numpy batches.

    Provides batches from a numpy array or a batch generator. Expects Bx3xHxW float32 in [0,1].
    """

    def __init__(
        self,
        batch_data: Optional[np.ndarray] = None,
        batch_generator: Optional[Callable[[], Iterable[np.ndarray]]] = None,
        cache_file: str = "robocaps_calib.cache",
        input_name: str = "images",
    ) -> None:
        if trt is None or cuda is None:
            raise RuntimeError("TensorRT/pycuda not available for INT8 calibration")
        self.cache_file = cache_file
        self.input_name = input_name
        if batch_data is not None:
            self.batches = iter(batch_data)
        elif batch_generator is not None:
            self.batches = iter(batch_generator())
        else:
            raise ValueError("Provide batch_data or batch_generator")
        self.device_input = None
        self.dims = None

    # TensorRT expects an object implementing IInt8EntropyCalibrator2
    def __getattr__(self, name):  # dynamic proxy for the TRT API
        if name == "get_batch":
            return self.get_batch
        if name == "get_batch_size":
            return self.get_batch_size
        if name == "read_calibration_cache":
            return self.read_calibration_cache
        if name == "write_calibration_cache":
            return self.write_calibration_cache
        raise AttributeError(name)

    def get_batch(self, names):  # names: list of input tensor names
        try:
            batch = next(self.batches)
        except StopIteration:
            return None
        if self.device_input is None:
            self.dims = batch.shape
            size = batch.nbytes
            self.device_input = cuda.mem_alloc(size)
        cuda.memcpy_htod(self.device_input, batch)
        return [int(self.device_input)]

    def get_batch_size(self) -> int:
        return self.dims[0] if self.dims is not None else 1

    def read_calibration_cache(self) -> bytes:
        try:
            with open(self.cache_file, "rb") as f:
                return f.read()
        except Exception:
            return b""

    def write_calibration_cache(self, cache: bytes) -> None:
        with open(self.cache_file, "wb") as f:
            f.write(cache)
