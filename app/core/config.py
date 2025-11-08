import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPilot"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Task management API with FastAPI by WillyPhan"
    AUTHOR: str = "Willy Phan"
    DATABASE_URL: str = "sqlite+aiosqlite:///./taskpilot.db"

    class Config:
        env_file = ".env"

settings = Settings()
