# app/services/ai_waiter_service.py

import re
from app.services.vector_service import query_menu
from app.services.session_store import get_session
from app.services.order_service import add_item, get_order, clear_order


# =========================
# SMART INTENT DETECTOR
# =========================
def detect_intent(text):
    text = text.lower()

    if any(x in text for x in ["menu", "show"]):
        return "SHOW_MENU"

    if any(x in text for x in ["veg"]):
        return "VEG"

    if any(x in text for x in ["nonveg", "non veg", "chicken", "mutton", "fish", "egg"]):
        return "NONVEG"

    if any(x in text for x in ["bill", "total", "order"]):
        return "SHOW_BILL"

    if any(x in text for x in ["confirm", "done", "place order"]):
        return "CONFIRM"

    if any(x in text for x in ["special", "suggest", "recommend"]):
        return "SUGGEST"

    return "ORDER_OR_QUERY"


def extract_qty(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else 1


def format_items(items):
    return "\n".join([f"• {i['name']} (₹{i['price']})" for i in items])


# =========================
# HUMAN-LIKE RESPONSE
# =========================
def human_reply(text):
    return f"🙂 {text}"


# =========================
# MAIN AI WAITER
# =========================
def run_ai_waiter(user_id: str, user_input: str):
    session = get_session(user_id)
    menu = query_menu("")
    text = user_input.lower()

    intent = detect_intent(text)

    # =========================
    # MENU
    # =========================
    if intent == "SHOW_MENU":
        return human_reply(
            "Here’s our menu:\n\n" + format_items(menu[:12]) +
            "\n\nWhat are you in the mood for?"
        )

    # =========================
    # VEG
    # =========================
    if intent == "VEG":
        veg = [i for i in menu if i["category"] == "veg"]

        return human_reply(
            "Sure, here are some veg options:\n\n" +
            format_items(veg[:10]) +
            "\n\nWould you like something spicy or light?"
        )

    # =========================
    # NONVEG
    # =========================
    if intent == "NONVEG":
        nonveg = [i for i in menu if i["category"] == "non-veg"]

        return human_reply(
            "Got it 👍 Here are some non-veg dishes:\n\n" +
            format_items(nonveg[:10]) +
            "\n\nBiryani or something grilled?"
        )

    # =========================
    # SUGGESTION (SMART)
    # =========================
    if intent == "SUGGEST":
        return human_reply(
            "Our popular picks today:\n\n"
            "• Chicken Biryani (₹250)\n"
            "• Chicken Tikka (₹240)\n"
            "• Paneer Butter Masala (₹180)\n\n"
            "Chicken or paneer — what do you prefer?"
        )

    # =========================
    # ORDER
    # =========================
    results = query_menu(user_input)

    if results:
        item = results[0]
        qty = extract_qty(user_input)

        add_item(user_id, item["name"], qty)

        # 💡 SMART UPSELL
        if "biryani" in item["name"].lower():
            return human_reply(
                f"Added {qty} {item['name']} 👍\n\n"
                "Would you like a drink or raita with that?"
            )

        return human_reply(
            f"Added {qty} {item['name']} to your order.\n\n"
            "Anything else?"
        )

    # =========================
    # BILL
    # =========================
    if intent == "SHOW_BILL":
        order = get_order(user_id)

        if not order:
            return human_reply("You haven’t ordered anything yet.")

        total = 0
        lines = []

        for i in order:
            price = i["price"] * i["qty"]
            total += price
            lines.append(f"{i['name']} x{i['qty']} — ₹{price}")

        return human_reply(
            "Here’s your order:\n\n" +
            "\n".join(lines) +
            f"\n\nTotal: ₹{total}\n\n"
            "Shall I place the order?"
        )

    # =========================
    # CONFIRM
    # =========================
    if intent == "CONFIRM":
        clear_order(user_id)

        return human_reply(
            "Done 👍 Your order has been placed.\n"
            "It’ll be ready shortly!"
        )

    # =========================
    # FALLBACK (VERY IMPORTANT)
    # =========================
    return human_reply(
        "Sorry, I didn’t get that.\n"
        "You can say things like 'chicken biryani', 'show menu', or 'bill'."
    )