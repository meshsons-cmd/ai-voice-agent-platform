from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import Base, engine
from app.models import Conversation, Message  # noqa: F401
from app.api.routes import router
from app.api.voice import router as voice_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins,
                   allow_credentials=True, allow_methods=["GET","POST"],
                   allow_headers=["Authorization","Content-Type"])
app.include_router(router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status":"ok","service":settings.app_name}
