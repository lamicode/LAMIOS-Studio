"""System hardware telemetry and RAM safety monitor for LAMIOS Studio."""

from __future__ import annotations

import platform
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class HardwareSnapshot:
    """Point-in-time snapshot of CPU, RAM, and execution environment telemetry."""

    os_name: str
    os_release: str
    architecture: str
    python_version: str
    cpu_physical_cores: int
    cpu_logical_cores: int
    cpu_percent: float
    ram_total_gb: float
    ram_available_gb: float
    ram_used_percent: float
    cuda_available: bool
    recommended_device: str
    ram_warning: bool


class HardwareMonitor:
    """Collects non-blocking hardware telemetry to protect 16 GB RAM CPU-only workstations."""

    def __init__(self, ram_warning_threshold_percent: float = 75.0) -> None:
        if not (10.0 <= ram_warning_threshold_percent <= 95.0):
            raise ValueError("ram_warning_threshold_percent must be between 10.0 and 95.0")
        self.ram_warning_threshold_percent = ram_warning_threshold_percent
        psutil.cpu_percent(interval=None)

    @staticmethod
    def detect_cuda_available() -> bool:
        """Safely detect NVIDIA CUDA availability without requiring PyTorch to be installed."""
        try:
            import torch  # type: ignore[import-not-found]

            return bool(torch.cuda.is_available())
        except Exception:
            return False

    def capture_snapshot(self) -> HardwareSnapshot:
        """Capture current CPU, memory, and device readiness metrics."""
        mem = psutil.virtual_memory()
        bytes_per_gb = 1024**3
        ram_total_gb = round(mem.total / bytes_per_gb, 2)
        ram_available_gb = round(mem.available / bytes_per_gb, 2)
        ram_used_percent = round(float(mem.percent), 1)
        cpu_percent = round(float(psutil.cpu_percent(interval=None)), 1)

        cuda_available = self.detect_cuda_available()
        recommended_device = "cuda" if cuda_available else "cpu"
        ram_warning = ram_used_percent >= self.ram_warning_threshold_percent

        return HardwareSnapshot(
            os_name=platform.system(),
            os_release=platform.release(),
            architecture=platform.machine(),
            python_version=platform.python_version(),
            cpu_physical_cores=psutil.cpu_count(logical=False) or 1,
            cpu_logical_cores=psutil.cpu_count(logical=True) or 1,
            cpu_percent=cpu_percent,
            ram_total_gb=ram_total_gb,
            ram_available_gb=ram_available_gb,
            ram_used_percent=ram_used_percent,
            cuda_available=cuda_available,
            recommended_device=recommended_device,
            ram_warning=ram_warning,
        )
