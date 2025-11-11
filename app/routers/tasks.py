from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ✅ CREATE
@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# ✅ READ ALL
@router.get("/", response_model=list[TaskOut])
async def get_tasks(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Task))
    return result.scalars().all()

# ✅ READ BY ID
@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task



# Admin-only endpoint
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), user=Depends(require_role("admin"))):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"message": f"Task {task_id} deleted"}

