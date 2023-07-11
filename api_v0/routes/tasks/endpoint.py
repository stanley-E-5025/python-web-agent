from fastapi import APIRouter, HTTPException
from database.operations import create_task, read_task, update_task, delete_task
from database.models import Task

router = APIRouter(tags=["task"], prefix="/task")

@router.post("/", response_model=Task)
def create_new_task(task: Task):
    return create_task(task)

@router.get("/{id}", response_model=Task)
def get_task(id: int):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{id}", response_model=Task)
def update_existing_task(id: int, task: Task):
    updated_task = update_task(id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{id}", response_model=Task)
def delete_existing_task(id: int):
    deleted_task = delete_task(id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
