# Containerized Task API

A containerized **FastAPI task management API** backed by **PostgreSQL**, with the entire application stack running through Docker Compose.

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

> On Windows PowerShell, you can use:
>
> ```powershell
> Copy-Item .env.example .env
> ```

### 3. Start the application

Build and start the entire stack with:

```bash
docker compose up --build
```

Once the containers are running:

* **API:** http://localhost:8000
* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

---

## 🏗️ Architecture

The application consists of two Docker services:

```text
┌─────────────────────┐
│     FastAPI API     │
│      Port 8000      │
└──────────┬──────────┘
           │
           │ PostgreSQL
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│      Port 5432      │
└─────────────────────┘
```

Docker Compose handles:

* FastAPI application
* PostgreSQL database
* Container networking
* Database configuration
* Service startup

---

## ⚙️ Environment Variables

Create a `.env` file from `.env.example`.

| Variable            | Description                  | Default                                   |
| ------------------- | ---------------------------- | ----------------------------------------- |
| `DATABASE_URL`      | PostgreSQL connection string | `postgresql://postgres:dev@db:5432/tasks` |
| `POSTGRES_USER`     | Database username            | `postgres`                                |
| `POSTGRES_PASSWORD` | Database password            | `dev`                                     |
| `POSTGRES_DB`       | Database name                | `tasks`                                   |

> **Note:** The default credentials are intended for local development. Use secure credentials when deploying to production.

---

## 📡 API Endpoints

| Method   | Endpoint      | Description                       | Status Codes        |
| -------- | ------------- | --------------------------------- | ------------------- |
| `GET`    | `/tasks`      | List all tasks                    | `200`               |
| `GET`    | `/tasks/{id}` | Get a task by ID                  | `200`, `404`        |
| `POST`   | `/tasks`      | Create a new task                 | `201`, `400`        |
| `PUT`    | `/tasks/{id}` | Update title or completion status | `200`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete a task                     | `204`, `404`        |

---

## 🧪 API Verification

### Get all tasks

Using PowerShell:

```powershell
curl.exe "http://localhost:8000/tasks"
```

Example response:

```json
[
  {
    "id": 2,
    "title": "Build FastAPI App",
    "done": true
  },
  {
    "id": 3,
    "title": "Containerize Stack with Postgres",
    "done": false
  },
  {
    "id": 4,
    "title": "Build FastAPI App",
    "done": false
  }
]
```

### Swagger UI

You can also test all endpoints interactively through:

```text
http://localhost:8000/docs
```

---

## 🗄️ Database Verification

To inspect the PostgreSQL database directly inside the running container:

```bash
docker exec -it task-api-db-1 psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

This allows you to verify that tasks created through the API are being persisted correctly in PostgreSQL.

---

## 🐳 Docker Commands

### Start the stack

```bash
docker compose up
```

### Build and start

```bash
docker compose up --build
```

### Run in detached mode

```bash
docker compose up -d
```

### Stop the stack

```bash
docker compose down
```

### Stop and remove volumes

```bash
docker compose down -v
```

> Removing volumes deletes the PostgreSQL data stored in the Docker volume.

### View running containers

```bash
docker compose ps
```

### View application logs

```bash
docker compose logs
```

### Follow logs

```bash
docker compose logs -f
```

---

## 📁 Project Structure

```text
task-api/
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── ...
```

> The exact structure may vary depending on the implementation.

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **Docker**
* **Docker Compose**
* **Pydantic**
* **SQLAlchemy**

---

## 🎯 Project Goals

This project demonstrates how to build and containerize a backend service with:

* RESTful API design
* CRUD operations
* FastAPI request validation
* PostgreSQL persistence
* Docker containerization
* Docker Compose orchestration
* Environment-based configuration
* API testing and database verification

---

## 📄 License

This project is intended for educational and development purposes.
