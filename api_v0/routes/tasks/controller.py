from sqlmodel import Session

from database.settings import engine
from database.models import Task
from database.models import Task, TaskStatus, TaskType
from typing import Optional
from sqlalchemy import VARCHAR, and_, cast, delete, insert, or_, select, update

from helpers.scrap_client import ScraperClient


async def create_task(
    id: Optional[str],
    url: Optional[str],
    title: str, 
    description: Optional[str],
    status: TaskStatus,
    type: TaskType,
    file: Optional[str],
    steps: Optional[str]
):
    with Session(engine) as session:
        task = Task(id=id , url=url, title=title, description=description, status=status, type=type, file=file, steps=steps)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    

def read_task(id: int):
    with Session(engine) as session:
        task = session.get(Task, id)
        return task

def update_task(id: int, task: Task):
    with Session(engine) as session:
        db_task = session.get(Task, id)
        if db_task is None:
            return None
        task_data = task.dict(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

def delete_task(id: int):
    with Session(engine) as session:
        task = session.get(Task, id)
        if task is None:
            return None
        session.delete(task)
        session.commit()
        return task
    
def read_all_tasks():
    with Session(engine) as session:
        tasks = session.query(Task).all()
        return tasks
    

async def run_bot(steps, case, data):
    scraper = ScraperClient(steps, case, data)
    results = await scraper.extract_blob()
    return results