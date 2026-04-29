from fastapi import APIRouter
from app.services.order_service import get_order
from app.services.qr_service import generate_qr

router = APIRouter()

@router.get("/")
def generate():
    order = get_order()
    path = generate_qr(order)
    return {"qr_path": path}