import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPilot"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Task management API with FastAPI by WillyPhan"
    AUTHOR: str = "Willy Phan"
    DATABASE_URL: str = "sqlite+aiosqlite:///./taskpilot.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"

settings = Settings()
