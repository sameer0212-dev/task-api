import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Connect CRUD to SQLite", False),
            ]
        )

    connection.commit()
    connection.close()
    
def get_all_tasks():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    connection.close()
    
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })
    return tasks

def get_task_by_id(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    connection.close()
    
    if row is None:
        return None
        
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }
    
def create_task(title: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, False)
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    
    return {
        "id": new_id,
        "title": title,
        "done": False
    }