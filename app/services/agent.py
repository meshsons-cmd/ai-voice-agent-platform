from sqlalchemy.orm import Session
from app.models import Conversation, Message
from app.services.llm import OpenAIProvider

class AgentService:
    def __init__(self, db: Session): self.db = db

    def run(self, text: str, conversation_id: str | None):
        conversation = self.db.get(Conversation, conversation_id) if conversation_id else None
        if conversation is None:
            conversation = Conversation()
            self.db.add(conversation)
            self.db.flush()
        history = self.db.query(Message).filter_by(conversation_id=conversation.id).order_by(Message.id).all()
        messages = [{"role":"system","content":"You are a helpful assistant. Use tools when useful."}]
        messages += [{"role":m.role,"content":m.content} for m in history[-20:]]
        messages.append({"role":"user","content":text})
        answer, calls = OpenAIProvider().respond(messages)
        self.db.add_all([
            Message(conversation_id=conversation.id, role="user", content=text),
            Message(conversation_id=conversation.id, role="assistant", content=answer)
        ])
        self.db.commit()
        return conversation.id, answer, calls
