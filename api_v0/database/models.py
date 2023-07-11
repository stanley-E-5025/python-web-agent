from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, func, DateTime
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlmodel.sql.sqltypes import GUID

class TaskStatus(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskType(Enum):
    blob = "blob"
    steps = "steps"

class Task(SQLModel, table=True):
    id: UUID = Field(
        sa_column=Column(
            "id",
            GUID(),
            server_default=func.gen_random_uuid(),
            unique=True,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            nullable=False,
        )
    )

    url: Optional[str] = Field(nullable=True)
    title: str
    description: Optional[str] = Field(nullable=True)
    status: TaskStatus = Field(default=TaskStatus.todo)
    type: TaskType = Field(default=TaskType.blob)
    file: Optional[str] = Field(nullable=True)
    steps: Optional[str] = Field(default=None)
