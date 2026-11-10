from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent import AgentService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        cid, answer, calls = AgentService(db).run(payload.message, payload.conversation_id)
        return ChatResponse(conversation_id=cid, answer=answer, tool_calls=calls)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Assistant request failed.") from exc
