import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_order(user_input: str):
    prompt = f"""
Extract food order details from the user input.

Return ONLY JSON in this format:
{{
  "items": [
    {{"name": "item name", "qty": number}}
  ]
}}

Rules:
- Convert words like "one", "two", "couple" → numbers
- If quantity not mentioned, assume 1
- Keep item names clean
- No extra text, only JSON

User input:
{user_input}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    text = response.json()["response"]

    try:
        return json.loads(text)
    except:
        return {"items": []}