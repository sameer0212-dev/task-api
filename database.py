import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 1. Create table using PostgreSQL SERIAL primary key
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)

            # 2. Check row count for conditional seeding
            cur.execute("SELECT COUNT(*) FROM tasks;")
            count = cur.fetchone()["count"]

            # 3. Seed exactly 3 tasks ONLY if empty
            if count == 0:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s);",
                    [
                        ("Learn FastAPI", False),
                        ("Build CRUD API", False),
                        ("Containerize Stack with Postgres", False),
                    ]
                )
        conn.commit()

def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
            return cur.fetchall()

def get_task_by_id(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            return cur.fetchone()

def create_task(title: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # RETURNING gives us the newly auto-generated Postgres ID directly
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                (title, False)
            )
            new_task = cur.fetchone()
        conn.commit()
        return new_task

def update_task(task_id: int, title: str, done: bool):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                (title, done, task_id)
            )
            updated_task = cur.fetchone()
        conn.commit()
        return updated_task

def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
            deleted = cur.rowcount > 0
        conn.commit()
        return deleted