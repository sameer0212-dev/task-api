from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task as db_update_task,
    delete_task as db_delete_task
)

app = FastAPI()
initialize_database()

class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str
    done: bool




@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def read_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201)
def create_task_endpoint(task_data: TaskCreate):
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    new_task = create_task(task_data.title.strip())
    return new_task


@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id: int, task_update: TaskUpdate):
    if not task_update.title or not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    updated = db_update_task(task_id, task_update.title.strip(), task_update.done)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int):
    success = db_delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return