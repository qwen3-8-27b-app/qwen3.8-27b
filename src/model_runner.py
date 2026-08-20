import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama


class ModelRunner:
    """Handles downloading and initializing local LLM inference using llama.cpp."""

    REPO_ID = "Qwen/Qwen3.8-27B-Instruct-GGUF"

    def __init__(
        self, filename: str, gpu_layers: int = -1, context_size: int = 8192
    ):
        self.filename = filename
        self.gpu_layers = (
            gpu_layers  # -1 offloads all layers to GPU (CUDA/Metal)
        )
        self.context_size = context_size
        self.model_path = None
        self.llm = None

    def download_model(self) -> str:
        """Downloads the designated model quantization file from Hugging Face if not cached."""
        print(
            f"[*] Checking local storage for model file: {self.filename}..."
        )
        # Saves to default huggingface cache directory ~/.cache/huggingface/hub/
        self.model_path = hf_hub_download(
            repo_id=self.REPO_ID,
            filename=self.filename,
            resume_download=True,
        )
        print(f"[+] Model ready at: {self.model_path}")
        return self.model_path

    def load_model(self):
        """Initializes the llama.cpp engine with GPU offloading."""
        if not self.model_path:
            self.download_model()

        print("[*] Initializing Qwen3.8-27B engine with GPU acceleration...")
        self.llm = Llama(
            model_path=self.model_path,
            n_gpu_layers=self.gpu_layers,
            n_ctx=self.context_size,
            verbose=False,
        )
        print("[+] Model loaded successfully into VRAM!")

    def generate_response(
        self, prompt: str, system_prompt: str = ""
    ) -> str:
        """Executes streaming/text generation for coding and chat prompts."""
        if not self.llm:
            raise RuntimeError("Model is not initialized. Call load_model() first.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.llm.create_chat_completion(
            messages=messages, temperature=0.2, max_tokens=2048
        )
        return response["choices"][0]["message"]["content"]
