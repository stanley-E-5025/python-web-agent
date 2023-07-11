from sqlmodel import SQLModel, Field
import enum
from datetime import datetime

class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskType(enum.Enum):
    blob = "blob"
    steps = "steps"


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = None
    title: str
    description: str = None
    status: TaskStatus = TaskStatus.todo
    steps: dict = None
    type: TaskType = TaskType.blob
    file: str = None
    tags: list[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
