from pydantic_settings import BaseSettings
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    AI_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    class Config:
        env_file = env_path

settings = Settings()