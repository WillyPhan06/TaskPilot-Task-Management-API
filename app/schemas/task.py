from pydantic import BaseModel
from typing import Optional

# Shared properties
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

# Create schema (client → server)
class TaskCreate(TaskBase):
    pass

# Update schema (client → server)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Response schema (server → client)
class TaskOut(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True  # allows reading ORM objects directly
