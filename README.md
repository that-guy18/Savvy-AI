# Savvy AI & ChatGem (Powered by Google Gemini)

An intelligent, modern AI chat application featuring both a responsive web interface (Flask + Glassmorphism UI) and an interactive command-line interface (CLI) powered by the official Google GenAI Python SDK (`google-genai`).

---

## 🚀 Features

- **Selected Model:** `gemini-3.5-flash-lite` (Blazing fast, verified working with low latency and reliable rate limits).
- **Auto-Failover Resilience:** Automatically falls back across active models (`gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-flash-lite-latest`) if temporary provider demand spikes occur.
- **Modern Web Interface:**
  - Glassmorphism design with animated floating particles.
  - Live Markdown rendering (headings, bullet points, numbered lists, blockquotes, code blocks, tables).
  - Code syntax styling.
  - Context-aware multi-turn conversation memory.
  - Quick-start suggestion chips.
  - Typing indicator and clear chat button.
- **Terminal CLI (`chat.py`):**
  - Interactive multi-turn chat directly in the terminal.
  - Commands: `clear` to reset context, `exit` or `quit` to exit.

---

## 🛠️ Setup & Installation

### 1. Requirements
Ensure Python 3.10+ is installed. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Verify your `.env` file contains your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

---

## 💻 Usage

### Run the Web Application
```bash
python main.py
```
Then open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Run the Terminal CLI
```bash
python chat.py
```

---

## 📁 Project Structure

```
chat_gem/
├── main.py              # Flask backend server with API endpoints
├── chat.py              # Interactive CLI chat assistant
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API key & model config)
├── templates/
│   └── index.html       # Web UI with glassmorphism & markdown support
├── static/
│   └── images/          # UI icons & assets
└── README.md            # Documentation
```

