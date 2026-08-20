import gradio as gr
from hardware_detector import HardwareDetector
from model_runner import ModelRunner
from quant_allocator import QuantAllocator


def launch_interface(runner: ModelRunner, hardware_info: str):
    """Creates and launches the local web UI for pair-programming."""
    system_instruction = (
        "You are Qwen3.8-27B, an expert software engineering assistant. "
        "Provide accurate, highly efficient, bug-free, and clean code solutions."
    )

    def chat_response(user_message, history):
        # Format conversation history
        full_prompt = user_message
        try:
            bot_reply = runner.generate_response(
                prompt=full_prompt, system_prompt=system_instruction
            )
            return bot_reply
        except Exception as e:
            return f"Error executing model: {str(e)}"

    custom_theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="slate",
    )

    with gr.Blocks(theme=custom_theme, title="Qwen3.8-27B Local Studio") as demo:
        gr.Markdown(
            """
            # 🚀 Qwen3.8-27B Local Pair Programmer
            ### Opus-Level Local Coding — Powered by your graphics card
            """
        )

        with gr.Accordion("💻 Hardware & Quantization Details", open=False):
            gr.Markdown(f"```\n{hardware_info}\n```")

        chatbot = gr.ChatInterface(
            fn=chat_response,
            textbox=gr.Textbox(
                placeholder="Ask Qwen to refactor code, fix bugs, or vibe-code a project...",
                container=False,
                scale=7,
            ),
            description="100% Local & Private. No code leaves your computer.",
        )

    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        share=False,
    )
