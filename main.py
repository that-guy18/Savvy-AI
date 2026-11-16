import os
import logging
import warnings
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

# Filter pydantic internal serialization notice from SDK
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    logger.warning("GEMINI_API_KEY is not set in environment or .env file.")

client = genai.Client(api_key=api_key) if api_key else None

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = [
    DEFAULT_MODEL,
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
]
FALLBACK_MODELS = list(dict.fromkeys(FALLBACK_MODELS))

SYSTEM_PROMPT = """
You are Savvy AI — a helpful, friendly, and smart AI assistant.

Guidelines:
- Keep your answers clear, helpful, direct, and easy to read.
- Use formatting (bullet points, bold text, code blocks) naturally when it improves clarity.
- Maintain a warm, friendly, and approachable tone.
- Do not mention Gemini or underlying AI providers/models unless specifically asked.
"""


def generate_chat_response(user_prompt: str, history: list = None) -> tuple[str, str]:
    """Generates a response using the API with automatic fallback across reliable models."""
    if not client:
        raise ValueError("API key is missing or invalid. Please check your .env configuration.")

    if history and isinstance(history, list) and len(history) > 0:
        contents = []
        for item in history:
            role = item.get("role", "user")
            content_text = item.get("content", "")
            if not content_text:
                continue
            gemini_role = "user" if role == "user" else "model"
            contents.append({"role": gemini_role, "parts": [{"text": content_text}]})
        contents.append({"role": "user", "parts": [{"text": user_prompt}]})
    else:
        contents = user_prompt

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
    )

    last_error = None
    for model_name in FALLBACK_MODELS:
        try:
            logger.info("Attempting generation with model: %s", model_name)
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            if response and response.text:
                return response.text, model_name
        except Exception as e:
            logger.warning("Model %s failed: %s", model_name, e)
            last_error = e

    raise RuntimeError(f"All available models failed. Last error: {last_error}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_prompt = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_prompt:
        return jsonify({"reply": "Please enter a message.", "success": False}), 400

    try:
        reply, used_model = generate_chat_response(user_prompt, history)
        return jsonify({
            "reply": reply,
            "success": True
        })
    except Exception as e:
        logger.error("Chat generation failed: %s", e)
        return jsonify({
            "reply": f"Sorry, I encountered an issue: {str(e)}",
            "success": False
        }), 500


@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "ready": bool(api_key),
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
