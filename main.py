import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from dotenv import load_dotenv

import database
from database import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task as db_update_task,
    delete_task as db_delete_task
)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Task API")
security = HTTPBearer()

@app.on_event("startup")
def startup_event():
    try:
        initialize_database()
    except Exception as e:
        print(f"Database connection issue: {e}")

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str
    done: bool

class AuthCredentials(BaseModel):
    email: EmailStr
    password: str

# --- AUTH DEPENDENCY ---

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        res = supabase.auth.get_user(token)
        if not res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        return res.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# --- AUTH ROUTES ---

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(creds: AuthCredentials):
    try:
        res = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        if not res.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"error": "Signup failed"}
            )
        return {
            "message": "User created successfully",
            "user": {
                "id": res.user.id,
                "email": res.user.email
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": str(e)}
        )

@app.post("/auth/login")
def login(creds: AuthCredentials):
    try:
        res = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        if not res.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail={"error": "Invalid login credentials"}
            )
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"error": "Invalid login credentials"}
        )

@app.get("/auth/me")
def get_profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

@app.post("/auth/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )

# --- PUBLIC ROUTES ---

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/auth/signup", "/auth/login", "/auth/me", "/auth/logout"]
    }

@app.get("/health")
def health_check():
    try:
        get_all_tasks()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "database": "disconnected", "error": str(e)}
        )

# --- PROTECTED TASK ROUTES ---

@app.get("/tasks")
def read_tasks(user = Depends(get_current_user)):
    return get_all_tasks()

@app.get("/tasks/{task_id}")
def read_task(task_id: int, user = Depends(get_current_user)):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201)
def create_task_endpoint(task_data: TaskCreate, user = Depends(get_current_user)):
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    new_task = create_task(task_data.title.strip())
    return new_task

@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id: int, task_update: TaskUpdate, user = Depends(get_current_user)):
    if not task_update.title or not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    updated = db_update_task(task_id, task_update.title.strip(), task_update.done)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, user = Depends(get_current_user)):
    success = db_delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return