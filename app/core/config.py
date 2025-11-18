import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPilot"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Task management API with FastAPI by WillyPhan"
    AUTHOR: str = "Willy Phan"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    model_config = ConfigDict(extra="allow")


settings = Settings()
