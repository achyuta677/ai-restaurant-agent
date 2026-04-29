from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.agent_service import run_agent
from app.services.ai_waiter_service import run_ai_waiter

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "guest"   # ✅ default user


@router.post("/")
def chat(req: ChatRequest):
    return {
        "response": run_agent(req.user_id, req.message)
    }

@router.post("/")
def chat(req: ChatRequest):
    return {
        "response": run_ai_waiter(req.user_id, req.message)
    }