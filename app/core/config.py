from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPilot"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Task management API"
    AUTHOR: str = "Willy Phan"

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./taskpilot.db")
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    class Config:
        env_file = ".env"   # for local dev
        env_file_encoding = 'utf-8'

settings = Settings()
