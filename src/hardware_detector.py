import os
import platform
import psutil
import subprocess


class HardwareDetector:
    """Detects system hardware capabilities including GPU VRAM and Apple Silicon Unified Memory."""

    def __init__(self):
        self.os_type = platform.system()
        self.is_apple_silicon = False
        self.vram_gb = 0.0
        self.system_ram_gb = psutil.virtual_memory().total / (1024**3)

        self._detect_hardware()

    def _detect_hardware(self):
        """Runs auto-detection based on OS and available graphics hardware."""
        if self.os_type == "Darwin":
            # Check for Apple Silicon (M1-M5)
            arch = platform.machine()
            if arch == "arm64":
                self.is_apple_silicon = True
                # Unified Memory treats RAM as available VRAM
                self.vram_gb = self.system_ram_gb * 0.75  # ~75% usable for Metal
        else:
            # Try detecting NVIDIA GPU via pynvml or nvidia-smi
            self.vram_gb = self._get_nvidia_vram()

    def _get_nvidia_vram(self) -> float:
        """Attempts to retrieve NVIDIA GPU VRAM in Gigabytes."""
        try:
            import pynvml

            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            if device_count > 0:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                pynvml.nvmlShutdown()
                return info.total / (1024**3)
        except Exception:
            pass

        # Fallback to nvidia-smi command line interface
        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.total",
                    "--format=csv,noheader,nounits",
                ],
                encoding="utf-8",
            )
            vram_mb = float(output.strip().split("\n")[0])
            return vram_mb / 1024.0
        except Exception:
            # Fallback when GPU is not detected
            return 0.0

    def get_specs(self) -> dict:
        """Returns a summary dictionary of detected system specifications."""
        return {
            "os": self.os_type,
            "is_apple_silicon": self.is_apple_silicon,
            "vram_gb": round(self.vram_gb, 2),
            "system_ram_gb": round(self.system_ram_gb, 2),
        }
