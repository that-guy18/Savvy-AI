import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
You are Savvy AI — a highly intelligent, thoughtful, and expressive assistant.

Your responses MUST:
- Be clear, structured, and well-formatted.
- Include paragraphs, lists, bullet points, or code blocks when helpful.
- Sound friendly, conversational, and professional.
- Explain concepts in detail when the user asks questions.
- Never reply with extremely short or generic answers.
- Always expand the user’s request with useful extra insights.
- Format output using Markdown.

Example response style:
---
Sure! Here's what you asked for:

**1. Explanation**
[Provide well-structured explanation.]

**2. Key Points**
- Bullet point 1
- Bullet point 2

**3. Summary**
[Short summary]

---
Always follow this level of clarity and formatting.
"""



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_prompt = data.get("message", "")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}"],
        )

        reply = response.text

        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
