# app/services/order_service.py

from collections import defaultdict

ORDERS = defaultdict(list)


def add_item(user_id: str, name: str, qty: int):
    # check if item already exists → increase qty
    for item in ORDERS[user_id]:
        if item["name"] == name:
            item["qty"] += qty
            return

    # else add new
    ORDERS[user_id].append({
        "name": name,
        "qty": qty,
        "price": get_price(name)
    })


def get_order(user_id: str):
    return ORDERS[user_id]


def clear_order(user_id: str):
    ORDERS[user_id] = []


# helper
def get_price(name):
    from app.services.vector_service import query_menu
    results = query_menu(name)
    if results:
        return results[0]["price"]
    return 0

