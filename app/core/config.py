from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPilot"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Task management API with FastAPI by WillyPhan"
    AUTHOR: str = "Willy Phan"

    model_config = ConfigDict(env_file=".env")

settings = Settings()
