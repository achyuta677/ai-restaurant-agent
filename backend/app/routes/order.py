from fastapi import APIRouter
from app.services.order_service import add_item, get_order, clear_order

router = APIRouter()

@router.post("/add")
def add(name: str, qty: int):
    add_item(name, qty)
    return {"message": "Item added"}

@router.get("/")
def view():
    return get_order()

@router.post("/clear")
def clear():
    clear_order()
    return {"message": "Order cleared"}