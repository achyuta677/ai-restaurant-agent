from langchain.tools import tool
from app.services.vector_service import query_menu


@tool("search_menu")
def search_menu(input: str) -> str:
    """
    Search menu items based on user query like veg, non-veg, spicy, breakfast, etc.
    """

    results = query_menu(input)

    if not results:
        return "No matching items found."

    response = []

    for item in results:
        text = (
            f"{item['name']} - ₹{item['price']} | "
            f"{item['category']} | {item['meal_type']} | "
            f"{item['spicy']} spicy | {item['oil']} oil | {item['type']}"
        )
        response.append(text)

    return "\n".join(response)