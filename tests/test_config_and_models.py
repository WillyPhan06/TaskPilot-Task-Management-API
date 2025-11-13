from app.core.config import settings
from app.models.task import Task
import os


def test_settings_load_env_values():
    # These values come from the repository .env file included in the workspace
    assert settings.PROJECT_NAME == "TaskPilot"
    assert settings.SECRET_KEY == os.getenv("SECRET_KEY")


def test_task_model_defaults():
    # Create an instance and ensure defaults are set
    t = Task(title="Sample", description="desc")
    assert hasattr(t, "id")
    assert t.title == "Sample"
    assert t.description == "desc"
    # default for completed should be False
    assert t.completed is None
