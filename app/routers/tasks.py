from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
def get_tasks():
    return {"message": "List of all tasks"}

@router.post("/")
def create_task():
    return {"message": "Task created successfully"}
