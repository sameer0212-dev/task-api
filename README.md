# Task API & Polite Scraper Workspace

A backend engineering monorepo containing projects focused on **REST API development, PostgreSQL, Docker containerization, and responsible web scraping**.

---

## 📂 Repository Layout

```text
task-api/
├── scraper/
│   ├── src/                  # Scraper modules & Pydantic models
│   ├── cache/                # Cached raw HTML files (git-ignored)
│   ├── output/               # JSON outputs & run report (git-ignored)
│   ├── main.py               # Scraper entrypoint
│   └── README.md             # Scraper-specific documentation
│
├── database.py               # FastAPI database configuration
├── main.py                   # FastAPI application entrypoint
├── Dockerfile                # FastAPI container definition
├── compose.yaml              # Docker Compose configuration
├── .env.example              # Environment variable template
├── .gitignore
└── README.md                 # Root workspace documentation
```

---

# 🛠️ Included Projects

## 1. 🕷️ Polite Web Scraper

Located in:

```text
/scraper
```

A resilient web scraping pipeline built to extract structured book data from **Books to Scrape** while following polite scraping practices.

### Features

* HTML fetching with `Requests`
* HTML parsing with `BeautifulSoup4`
* Pydantic-based data validation
* Local HTML caching
* Rate limiting between requests
* Structured JSON output
* Run/report generation
* Resilient scraping workflow

### Tech Stack

* Python 3
* Requests
* BeautifulSoup4
* Pydantic

### Quick Run

From the repository root:

```bash
python scraper/main.py
```

For detailed scraper architecture, execution instructions, rate-limiting behavior, and schema definitions, see:

```text
scraper/README.md
```

---

# 2. 🚀 Containerized Task API

A RESTful **FastAPI task management service** backed by **PostgreSQL**.

The complete application stack runs through **Docker Compose**, making the API and database easy to build and run consistently across environments.

### Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Docker
* Docker Compose

---

## ⚡ Quick Start

### 1. Configure environment variables

Create your local `.env` file from the provided template:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 2. Build and start the stack

```bash
docker compose up --build
```

### 3. Access the API

Once the containers are running:

| Service    | URL                         |
| ---------- | --------------------------- |
| API        | http://localhost:8000       |
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

Swagger UI can be used to interactively test all API endpoints.

---

# ⚙️ Task API Environment Variables

Create a `.env` file using `.env.example`.

| Variable            | Description                  | Default                                   |
| ------------------- | ---------------------------- | ----------------------------------------- |
| `DATABASE_URL`      | PostgreSQL connection string | `postgresql://postgres:dev@db:5432/tasks` |
| `POSTGRES_USER`     | PostgreSQL username          | `postgres`                                |
| `POSTGRES_PASSWORD` | PostgreSQL password          | `dev`                                     |
| `POSTGRES_DB`       | PostgreSQL database name     | `tasks`                                   |

> **Note:** These default credentials are intended for local development. Use secure credentials for production deployments.

---

# 📡 Task API Endpoints

| Method   | Endpoint      | Description                       | Status Codes        |
| -------- | ------------- | --------------------------------- | ------------------- |
| `GET`    | `/tasks`      | List all tasks                    | `200`               |
| `GET`    | `/tasks/{id}` | Get a task by ID                  | `200`, `404`        |
| `POST`   | `/tasks`      | Create a new task                 | `201`, `400`        |
| `PUT`    | `/tasks/{id}` | Update title or completion status | `200`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete a task                     | `204`, `404`        |

---

# 🧪 API Verification

### Get all tasks

Using cURL:

```bash
curl "http://localhost:8000/tasks"
```

On Windows PowerShell, you can use:

```powershell
curl.exe "http://localhost:8000/tasks"
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Build FastAPI App",
    "done": true
  },
  {
    "id": 2,
    "title": "Containerize Stack with Postgres",
    "done": false
  }
]
```

You can also test the API directly through:

```text
http://localhost:8000/docs
```

---

# 🐳 Useful Docker Commands

### Build and start the Task API

```bash
docker compose up --build
```

### Run in detached mode

```bash
docker compose up -d
```

### View running containers

```bash
docker compose ps
```

### View logs

```bash
docker compose logs
```

### Follow logs

```bash
docker compose logs -f
```

### Stop the stack

```bash
docker compose down
```

### Stop the stack and remove database volumes

```bash
docker compose down -v
```

> ⚠️ Removing volumes deletes the PostgreSQL data stored in Docker volumes.

---

# 🗄️ Database Verification

The PostgreSQL database can be inspected directly from inside the running database container.

For example:

```bash
docker exec -it task-api-db-1 \
psql -U postgres -d tasks \
-c "SELECT * FROM tasks;"
```

This can be used to verify that tasks created through the API are correctly persisted in PostgreSQL.

---

# 🎯 Learning Objectives

This workspace demonstrates practical backend engineering concepts including:

* REST API development
* CRUD operations
* FastAPI application structure
* Request and response validation
* PostgreSQL database integration
* Docker containerization
* Docker Compose orchestration
* Environment-based configuration
* HTTP requests and HTML parsing
* Pydantic data validation
* Web scraping with rate limiting
* Local caching
* Structured data extraction
* Backend project organization

---

# 📌 Project Status

This repository serves as a backend engineering workspace containing progressively developed projects and assignments.

Each project has its own implementation and can be run independently according to its respective documentation.
