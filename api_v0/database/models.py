from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID,uuid4
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlmodel.sql.sqltypes import GUID
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, func


class TaskStatus(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskType(Enum):
    blob = "blob"
    steps = "steps"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(
        sa_column=Column(
            "id",
            GUID(),
            server_default=func.gen_random_uuid(),
            unique=True,
            primary_key=True,
        )
    )

    url: Optional[str] = Field(nullable=True)
    title: str
    description: Optional[str] = Field(nullable=True)
    status: TaskStatus = Field(default=TaskStatus.todo)
    type: TaskType = Field(default=TaskType.blob)
    file: Optional[str] = Field(nullable=True)
    steps: Optional[str] = Field(default=None)


    class Read(BaseModel):
            id: UUID
            url: Optional[str] 
            title: str
            description: Optional[str]
            status: TaskStatus
            type: TaskType
            file: Optional[str]
            steps: Optional[str]

