from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Voice Agent Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./voice_agent.db"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_transcribe_model: str = "gpt-4o-mini-transcribe"
    openai_speech_model: str = "gpt-4o-mini-tts"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
