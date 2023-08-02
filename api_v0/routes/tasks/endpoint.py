from fastapi import APIRouter, HTTPException, Form
from .controller import create_task, read_task, update_task, delete_task, read_all_tasks, run_bot
from database.models import Task, TaskStatus, TaskType
from helpers.scrap_client import ScraperClient
from utils.scraping import delete_directory, detect_encoding
import json
from uuid import UUID, uuid4
from config import POC_STEPS
import io
from fastapi.responses import StreamingResponse

import logging

import os
import pandas as pd
import base64
from typing import Optional
import asyncio




router = APIRouter(tags=["task"], prefix="/task")


logger = logging.getLogger(__name__)

@router.post("/", response_model=Task.Read)
async def create_new_task(
    url: Optional[str] = Form(...),
    title: str = Form(...), 
    description: Optional[str] = Form(...),
    status: TaskStatus = Form(...),
    type: TaskType = Form(...),
    file: Optional[str] = Form(...),
    steps: Optional[str] = Form(...)
):

    return await create_task(id= str(uuid4()), url=url, title=title, description=description, status=status, type=type, file=file, steps=steps)


@router.get("/{id}", response_model=Task)
def get_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/download/{id}")
def download_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.file:
        csv_base64_bytes = task.file.encode()
        csv_data_bytes = base64.b64decode(csv_base64_bytes)
        csv_data_str = csv_data_bytes.decode()

        response = StreamingResponse(io.StringIO(csv_data_str),
                                      media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response

    return HTTPException(status_code=404, detail="File not found")


@router.get("/", response_model=list[Task])
def get_all_tasks():
    return read_all_tasks()

def update_existing_task(id:UUID, task: Task):
    updated_task = update_task(id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{id}", response_model=Task)
def delete_existing_task(id:UUID):
    deleted_task = delete_task(id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task


@router.post("/execute/{id}", response_model=Task)
async def execute_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    type = task.type
    steps = json.loads(task.steps) 

    results = await run_bot(steps=steps, case=type, data="")
    download_dir = results

    csv_file = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
    if csv_file:
        csv_file_path = os.path.join(download_dir, csv_file[0])
        encoding = detect_encoding(csv_file_path)
        df = pd.read_csv(csv_file_path, encoding=encoding, sep="\t")

        csv_data_bytes = df.to_csv(index=False).encode()
        csv_base64_bytes = base64.b64encode(csv_data_bytes)
        csv_base64_str = csv_base64_bytes.decode()

        task.file = csv_base64_str
        update_task(id, task)
        delete_directory(download_dir)

    return task
