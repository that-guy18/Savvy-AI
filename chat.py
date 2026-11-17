import os
import sys
import warnings

# Ensure UTF-8 output handling and ANSI color processing on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if os.name == "nt":
    os.system("")

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Filter pydantic internal serialization notice from SDK
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("[Error] GEMINI_API_KEY is not set in environment or .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Working model choice with fallback
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = [
    DEFAULT_MODEL,
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
]
FALLBACK_MODELS = list(dict.fromkeys(FALLBACK_MODELS))

SYSTEM_PROMPT = """You are Savvy AI — a highly intelligent, thoughtful, and expressive AI assistant.
Provide clear, structured, and insightful answers. Format code blocks and lists cleanly using Markdown."""

# ANSI Color Codes for Modern Dark Terminal Styling
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_CYAN = "\033[1;36m"
C_INDIGO = "\033[1;38;5;99m"
C_PURPLE = "\033[1;35m"
C_GREEN = "\033[1;32m"
C_GRAY = "\033[38;5;244m"
C_YELLOW = "\033[1;33m"
C_WHITE = "\033[1;37m"


def send_chat_message(history: list, user_message: str) -> tuple[str, str]:
    """Sends a message with full conversation history and model fallback."""
    if history and len(history) > 0:
        contents = []
        for turn in history:
            gemini_role = "user" if turn["role"] == "user" else "model"
            contents.append({"role": gemini_role, "parts": [{"text": turn["content"]}]})
        contents.append({"role": "user", "parts": [{"text": user_message}]})
    else:
        contents = user_message

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
    )

    last_error = None
    for model_name in FALLBACK_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            if response and response.text:
                return response.text, model_name
        except Exception as e:
            last_error = e

    raise RuntimeError(f"All fallback models failed. Last error: {last_error}")


def main():
    print()
    print(f" {C_INDIGO}╭─────────────────────────────────────────────────────────────╮{C_RESET}")
    print(f" {C_INDIGO}│{C_RESET}  {C_BOLD}{C_WHITE}SAVVY AI{C_RESET} {C_PURPLE}✦{C_RESET} {C_GRAY}Next-Gen Intelligent Assistant{C_RESET}              {C_INDIGO}│{C_RESET}")
    print(f" {C_INDIGO}│{C_RESET}  {C_GRAY}Model:{C_RESET} {C_CYAN}{DEFAULT_MODEL}{C_RESET}  {C_GRAY}•{C_RESET}  {C_GRAY}Status:{C_RESET} {C_GREEN}● Online{C_RESET}                   {C_INDIGO}│{C_RESET}")
    print(f" {C_INDIGO}│{C_RESET}  {C_DIM}Type {C_RESET}{C_YELLOW}clear{C_RESET}{C_DIM} to reset context, {C_RESET}{C_YELLOW}exit{C_RESET}{C_DIM} or {C_RESET}{C_YELLOW}quit{C_RESET}{C_DIM} to leave{C_RESET}       {C_INDIGO}│{C_RESET}")
    print(f" {C_INDIGO}╰─────────────────────────────────────────────────────────────╯{C_RESET}")
    print()

    history = []

    while True:
        try:
            user_input = input(f" {C_CYAN}You ›{C_RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n {C_GRAY}Session closed. Have a great day!{C_RESET}\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(f"\n {C_GRAY}Session closed. Have a great day!{C_RESET}\n")
            break

        if user_input.lower() == "clear":
            history.clear()
            print(f"\n {C_YELLOW}⚡ Conversation context reset.{C_RESET}\n")
            continue

        print(f" {C_GRAY}Thinking...{C_RESET}", end="\r", flush=True)

        try:
            reply, model_used = send_chat_message(history, user_input)
            print(" " * 30, end="\r", flush=True)
            print(f" {C_PURPLE}Savvy AI{C_RESET} {C_DIM}({model_used}){C_RESET}:")
            print(f"{C_WHITE}{reply}{C_RESET}")
            print(f" {C_GRAY}{'─' * 60}{C_RESET}\n")

            history.append({"role": "user", "content": user_input})
            history.append({"role": "model", "content": reply})

        except Exception as e:
            print(" " * 30, end="\r", flush=True)
            print(f" \033[1;31m[Error]\033[0m {e}\n")


if __name__ == "__main__":
    main()
