from langchain.tools import tool
from app.services.order_service import get_order
from app.services.qr_service import generate_qr


@tool("generate_order_qr")
def generate_order_qr(input: str) -> str:
    """
    Generate a QR code for the current order.
    """

    order = get_order()

    if not order:
        return "Order is empty. Add items first."

    path = generate_qr(order)

    return f"QR generated successfully at: {path}"