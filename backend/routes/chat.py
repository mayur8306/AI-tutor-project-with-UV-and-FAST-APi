from fastapi import APIRouter, Depends
from backend.auth.deps import get_current_user
from backend.services.tutor import get_reply
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, user_id=Depends(get_current_user)):
    try:
        print("CHAT ROUTE HIT")
        reply = get_reply(req.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        print(" ROUTE ERROR:", repr(e))
        raise
