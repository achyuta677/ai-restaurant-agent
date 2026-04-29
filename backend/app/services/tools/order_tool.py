from langchain.tools import tool
from app.services.order_service import add_item, get_order, clear_order
from app.services.parser_service import parse_order
from app.services.vector_service import query_menu


def validate_item(name: str):
    results = query_menu(name)
    if results:
        return results[0]["name"]
    return None


@tool("add_to_order")
def add_to_order(input: str) -> str:
    """
    Add items to order from natural language input.
    Example: 'add two chicken curry and 1 naan'
    """

    parsed = parse_order(input)

    if not parsed["items"]:
        return "Sorry, I couldn't understand the order."

    added_items = []
    not_found_items = []

    for item in parsed["items"]:
        name = item["name"]
        qty = item["qty"]

        valid_name = validate_item(name)

        if not valid_name:
            not_found_items.append(name)
            continue

        add_item(valid_name, qty)
        added_items.append(f"{qty} x {valid_name}")

    response = ""

    if added_items:
        response += "Added: " + ", ".join(added_items)

    if not_found_items:
        response += "\nNot found: " + ", ".join(not_found_items)

    return response


@tool("view_order")
def view_order(input: str) -> str:
    """
    View current order items.
    """

    order = get_order()

    if not order:
        return "Your order is empty."

    return str(order)


@tool("clear_all")
def clear_all(input: str) -> str:
    """
    Clear the entire order.
    """

    clear_order()
    return "Order cleared."