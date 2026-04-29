# AI Restaurant Agent Backend

A FastAPI backend for an AI-powered restaurant ordering assistant. This service provides chat interaction, semantic menu search, order management, and QR code generation based on an in-memory restaurant menu.

## 🚀 Project Overview

This backend is designed to power an AI restaurant agent that can:
- respond to conversational requests about the menu
- add menu items to a user order
- display current orders and billing
- generate a QR code for an order
- use semantic similarity search for menu matching

## 📁 Project Structure

- `run.py` - entry point for local development
- `app/main.py` - FastAPI application setup and route registration
- `app/routes/` - API endpoint routers for chat, order, and QR
- `app/services/` - business logic, AI processing, session management, QR generation, and menu search
- `app/data/menu.json` - restaurant menu dataset

## 🔧 Key Features

- FastAPI REST API with CORS enabled
- Semantic menu search using `sentence-transformers`
- Simple in-memory session and order storage
- AI waiter interaction layer with intent detection
- QR code generation for order payloads
- Integration points for Groq and Ollama LLM services

## 📦 Dependencies

This project depends on the following Python packages:

- `fastapi`
- `uvicorn`
- `sentence-transformers`
- `numpy`
- `qrcode`
- `requests`
- `groq`

> The repository currently does not include a populated `requirements.txt`, so install the above packages manually or generate a dependency list from your environment.

## ⚙️ Environment Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install fastapi uvicorn sentence-transformers numpy qrcode requests groq
```

3. Set required environment variables:
- `GROQ_API_KEY` - API key for Groq chat completions

4. Ensure an Ollama-compatible LLM API is available at:
- `http://localhost:11434`

## ▶️ Run Locally

From the `backend` folder, start the app with:
```bash
python run.py
```

The service will start on `http://127.0.0.1:8000` by default.

## 🧪 API Endpoints

### Health Check

- `GET /`
- Response: `{ "message": "AI Restaurant Agent Running 🚀" }`

### Chat

- `POST /chat/`
- Body JSON:
  - `message`: user text
  - `user_id`: optional, default `guest`

Example request:
```json
{
  "message": "Show me veg options",
  "user_id": "guest"
}
```

### Order Management

- `POST /order/add?name=<item>&qty=<qty>`
- `GET /order/`
- `POST /order/clear`

### QR Code Generation

- `GET /qr/`
- Generates `order_qr.png` and returns its relative path

## 📌 Notes / Implementation Details

- `app/services/vector_service.py` loads `app/data/menu.json` and builds semantic embeddings on startup.
- The chat flow is intended to support both Groq-based AI chat and a simpler rule-based `ai_waiter` flow.
- Order state is stored in memory using `collections.defaultdict`; restarting the service resets all orders.
- QR code output is written to `order_qr.png` in the backend folder.

## ⚠️ Known limitations

- `app/routes/chat.py` currently defines two `POST` handlers for the same endpoint, so the second handler overrides the first. That means the active chat behavior is the `ai_waiter` flow.
- No persistent database is configured; all sessions and orders are volatile.
- `requirements.txt` is empty and should be updated before deployment.

## 💡 Future Improvements

- Add persistent storage for orders and sessions
- Expose separate endpoints for menu search and chat
- Add frontend integration and authentication
- Improve LLM prompt design and fallback handling
- Add Docker support

---

Created for the AI Restaurant Agent backend in `d:\ai-restaurant-agent\backend`.
