from fastapi import APIRouter
from .tasks.endpoint import router as tasks_router


central_router = APIRouter()
central_router.include_router(router=tasks_router)


