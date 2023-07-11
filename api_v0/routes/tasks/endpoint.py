from fastapi import APIRouter, HTTPException
from database.operations import create_task, read_task, update_task, delete_task, read_all_tasks
from database.models import Task
from helpers.scrap_client import ScraperClient
from utils.scraping import delete_directory, detect_encoding
import json
from uuid import UUID
from config import POC_STEPS
import io


import os
import pandas as pd
import base64


router = APIRouter(tags=["task"], prefix="/task")

@router.post("/", response_model=Task)
def create_new_task(task: Task):
    return create_task(task)


@router.get("/{id}", response_model=Task)
def get_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.file:
        csv_base64_bytes = task.file.encode()
        csv_data_bytes = base64.b64decode(csv_base64_bytes)
        csv_data_str = csv_data_bytes.decode()
        data = io.StringIO(csv_data_str)
        df = pd.read_csv(data)

        print(df)  # or return, or process as needed

    return task


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

    url = task.url
    type = task.type

    scraper = ScraperClient(url, POC_STEPS, type, task.id)
    results = await scraper.extract_blob()

    
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
