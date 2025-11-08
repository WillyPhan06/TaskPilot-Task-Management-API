from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.task import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
async def create_task(title: str, description: str = "", db: AsyncSession = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks
