import os
import json
from groq import Groq

from app.services.order_service import add_item, get_order, clear_order
from app.services.vector_service import query_menu
from app.services.session_store import get_session


# =========================
# GROQ CLIENT
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================
# TOOLS (FUNCTIONS)
# =========================

def add_to_order(user_id, name, qty):
    add_item(user_id, name, qty)
    return f"Added {name} x{qty}"


def remove_from_order(user_id, name):
    order = get_order(user_id)

    for item in order:
        if name.lower() in item["name"].lower():
            order.remove(item)
            return f"Removed {item['name']}"

    return "Item not found"


def get_bill(user_id):
    order = get_order(user_id)

    if not order:
        return "Your order is empty."

    total = 0
    lines = []

    for i in order:
        price = i["price"] * i["qty"]
        total += price
        lines.append(f"{i['name']} x{i['qty']} = ₹{price}")

    return "\n".join(lines) + f"\nTotal = ₹{total}"


# =========================
# TOOL MAP
# =========================
TOOLS = {
    "add_item": add_to_order,
    "remove_item": remove_from_order,
    "get_bill": get_bill,
}


# =========================
# SYSTEM PROMPT (VERY IMPORTANT)
# =========================
SYSTEM_PROMPT = """
You are a smart restaurant waiter AI.

Rules:
- Understand natural language (English, Hindi, Odia)
- Always be friendly and conversational
- If user wants food → call add_item
- If removing → call remove_item
- If asking bill → call get_bill
- Suggest add-ons like a real waiter
- If user says "yes", use previous context
- Never hallucinate items not in menu
- Use menu data only

Respond in short natural sentences.
"""


# =========================
# MAIN AGENT
# =========================

def run_agent(user_id: str, user_input: str):
    session = get_session(user_id)

    # get menu
    menu = query_menu("")
    menu_text = "\n".join([f"{i['name']} - ₹{i['price']}" for i in menu])

    # conversation memory
    history = session.get("history", [])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"MENU:\n{menu_text}"},
    ] + history + [
        {"role": "user", "content": user_input}
    ]

    # =========================
    # GROQ CALL
    # =========================
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ working model
        messages=messages,
        temperature=0.7,
    )

    reply = response.choices[0].message.content

    # =========================
    # SAVE MEMORY
    # =========================
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-10:]  # keep last 10

    return reply