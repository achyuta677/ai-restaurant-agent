import requests
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



# 🔥 Try models in order (auto fallback)
MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama3-8b-8192",
    "mixtral-8x7b-32768"
]


def ask_ai(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    for model in MODELS:
        try:
            print(f"🔄 Trying model: {model}")

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a smart restaurant waiter."},
                    {"role": "user", "content": prompt}
                ]
            }

            res = requests.post(url, headers=headers, json=data, timeout=8)
            result = res.json()

            print("🔍 RESPONSE:", result)

            # ✅ SUCCESS
            if "choices" in result:
                print(f"✅ Using model: {model}")
                return result["choices"][0]["message"]["content"]

            # ❌ model error → try next
            if "error" in result:
                print(f"❌ Model failed: {model} → {result['error']['message']}")
                continue

        except Exception as e:
            print(f"⚠️ Exception with {model}:", e)
            continue

    # 🚨 If ALL models fail
    return (
        "⚠️ AI service is currently unavailable.\n"
        "But I can still help you with menu and orders.\n"
        "Try: show menu / veg items / add food"
    )