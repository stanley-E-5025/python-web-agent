from fastapi import APIRouter, UploadFile, File, Form
router = APIRouter(tags=["task"], prefix="/task")


@router.get("/get_tasks")
async def get_tasks():
    return {"message": "Hello World"}


@router.post("/create_task")
async def create_task():
    return {"message": "Hello World"}


@router.get("/get_task/{task_id}")
async def get_task(
    task_id: int,
):
    return {"message": "Hello World"}


@router.put("/update_task/{task_id}")
async def update_task(
    task_id: int,
):
    return {"message": "Hello World"}


@router.delete("/delete_task/{task_id}")
async def delete_task(
    task_id: int,
):
    return {"message": "Hello World"}
