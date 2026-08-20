from typing import Dict, Tuple


class QuantAllocator:
    """Determines the optimal GGUF quantization level based on available system hardware."""

    # Qwen3.8-27B GGUF quantization options mapped to required memory and file tags
    QUANT_MAPPING = {
        "FP8": {
            "quant": "Q8_0",
            "file": "Qwen3.8-27B-Instruct-Q8_0.gguf",
            "vram_required": 18.0,
        },
        "Q4_K_M": {
            "quant": "Q4_K_M",
            "file": "Qwen3.8-27B-Instruct-Q4_K_M.gguf",
            "vram_required": 11.5,
        },
        "IQ3_M": {
            "quant": "IQ3_M",
            "file": "Qwen3.8-27B-Instruct-IQ3_M.gguf",
            "vram_required": 7.5,
        },
        "IQ2_XXS": {
            "quant": "IQ2_XXS",
            "file": "Qwen3.8-27B-Instruct-IQ2_XXS.gguf",
            "vram_required": 5.0,
        },
    }

    @classmethod
    def select_best_quant(cls, hardware_specs: Dict) -> Tuple[str, str, str]:
        """Returns (quant_name, filename, recommended_reason) based on hardware capability."""
        vram = hardware_specs["vram_gb"]
        is_mac = hardware_specs["is_apple_silicon"]

        if vram >= 16.0:
            choice = "FP8"
            reason = "Optimal performance (16GB+ VRAM detected). Running high-precision quantization."
        elif vram >= 11.0:
            choice = "Q4_K_M"
            reason = "Standard sweet spot (12GB VRAM detected). Balanced speed and reasoning quality."
        elif vram >= 7.0:
            choice = "IQ3_M"
            reason = "Low-bit optimized quant (8GB VRAM detected). Fits comfortably in memory."
        else:
            choice = "IQ2_XXS"
            reason = "Extreme low-bit quant. Fallback for constrained hardware setups."

        if is_mac:
            reason += " Native Apple Silicon Metal acceleration enabled."

        selected = cls.QUANT_MAPPING[choice]
        return selected["quant"], selected["file"], reason
