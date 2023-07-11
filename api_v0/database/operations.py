from sqlmodel import Session

from .settings import engine
from .models import Task

def create_task(task: Task):
    with Session(engine) as session:
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
