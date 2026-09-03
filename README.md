# Task API, LLM Enrichment & Polite Scraper Workspace

A backend engineering monorepo containing projects focused on **REST API development, asynchronous LLM enrichment pipelines, PostgreSQL, Docker containerization, automated evaluation, and responsible web scraping**.

---

## 📂 Repository Layout

```text
task-api/
├── app/
│   ├── llm/
│   │   ├── client.py              # Async LLM client & defensive response parsing
│   │   └── schemas.py             # Pydantic schemas & BookCategory enums
│   │
│   ├── routes/
│   │   └── llm_enrich.py          # POST /llm/enrich endpoint
│   │
│   └── __init__.py
│
├── evals/
│   ├── cases.json                 # Benchmark test cases
│   └── run_eval.py                # Automated evaluation harness
│
├── prompts/
│   └── enrich-v1.md               # Versioned enrichment system prompt
│
├── scraper/
│   ├── src/                       # Scraper modules & Pydantic models
│   ├── cache/                     # Cached HTML files (git-ignored)
│   ├── output/                    # JSON outputs & run reports (git-ignored)
│   ├── main.py                    # Scraper entrypoint
│   └── README.md                  # Scraper-specific documentation
│
├── database.py                    # FastAPI database configuration
├── main.py                        # FastAPI application entrypoint
├── Dockerfile                     # FastAPI container definition
├── compose.yaml                   # Docker Compose configuration
├── .env.example                   # Environment variable template
├── .gitignore
└── README.md                      # Root workspace documentation
```

---

# 🛠️ Included Projects

## 1. 🧠 LLM Book Enrichment Service & Evals

An asynchronous LLM-powered classification and metadata extraction pipeline that transforms raw book titles and descriptions into structured metadata.

The enrichment service produces:

* Normalized book categories
* Classification confidence scores
* Key thematic tags
* One-sentence summaries
* Quality indicators

### Features

#### Strict Structured Output Parsing

LLM responses are validated against Pydantic `EnrichResponse` schemas to ensure predictable structured output.

#### Resilient Retry & Fallback Routing

The service handles transient failures such as rate limits and timeouts using retry logic with exponential backoff.

Unknown or invalid categories are normalized to:

```text
Other
```

#### Quarantine Logging

Unparseable or malformed upstream LLM responses are captured in:

```text
logs/quarantine.jsonl
```

This prevents malformed model output from unnecessarily causing `500 Internal Server Error` responses.

#### Automated Evaluation Harness

The evaluation suite tests the enrichment pipeline against multiple benchmark cases, including:

* Fiction vs. non-fiction classification
* Edge cases
* Ambiguous content
* Structured output compliance
* Fallback behavior

---

# 2. 🚀 Containerized Task API

A RESTful **FastAPI task management service** backed by **PostgreSQL**.

The application and database are orchestrated through **Docker Compose**, providing a reproducible development environment.

### Tech Stack

* Python 3.11+
* FastAPI
* AsyncOpenAI
* PostgreSQL
* SQLAlchemy
* Pydantic v2
* Docker
* Docker Compose

---

# 3. 🕷️ Polite Web Scraper

Located in:

```text
/scraper
```

A resilient scraping pipeline designed to extract structured book data from **Books to Scrape** while following responsible scraping practices.

### Features

* HTTP requests with `Requests`
* HTML parsing with `BeautifulSoup4`
* Pydantic data validation
* Rate limiting
* Local HTML caching
* Structured JSON output
* Run reports
* Resilient extraction pipeline

For scraper-specific execution instructions and implementation details, see:

```text
scraper/README.md
```

---

# ⚡ Quick Start

## 1. Configure Environment Variables

Create your local `.env` file from the provided template.

### PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

If you want to test the LLM enrichment service, make sure your LLM credentials are configured in `.env`.

---

## 2. Build and Start the Stack

```bash
docker compose up --build
```

Docker Compose will build the API container and start the required services, including PostgreSQL.

---

## 3. Access the API

Once the containers are running:

| Service    | URL                         |
| ---------- | --------------------------- |
| API        | http://localhost:8000       |
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

Swagger UI provides an interactive interface for testing the available API endpoints.

---

# ⚙️ Environment Variables

Create a `.env` file using `.env.example`.

| Variable       | Description                             | Default                                   |
| -------------- | --------------------------------------- | ----------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string            | `postgresql://postgres:dev@db:5432/tasks` |
| `LLM_API_KEY`  | API key for the configured LLM provider | `your_api_key_here`                       |
| `LLM_BASE_URL` | Base URL for the LLM provider           | `https://openrouter.ai/api/v1`            |
| `LLM_MODEL`    | Target LLM model                        | `openrouter/free`                         |

> **Security:** Never commit `.env` or API keys to version control.

---

# 📡 API Endpoints

## LLM Enrichment

| Method | Endpoint      | Description                                          | Status Codes        |
| ------ | ------------- | ---------------------------------------------------- | ------------------- |
| `POST` | `/llm/enrich` | Classify and enrich a raw book title and description | `200`, `422`, `500` |

## Task Management

| Method   | Endpoint      | Description                       | Status Codes        |
| -------- | ------------- | --------------------------------- | ------------------- |
| `GET`    | `/tasks`      | List all tasks                    | `200`               |
| `GET`    | `/tasks/{id}` | Get a task by ID                  | `200`, `404`        |
| `POST`   | `/tasks`      | Create a new task                 | `201`, `400`        |
| `PUT`    | `/tasks/{id}` | Update title or completion status | `200`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete a task                     | `204`, `404`        |

---

# 🧪 Automated Evaluation

The repository includes an automated evaluation harness for validating the LLM enrichment pipeline.

Run the benchmark suite with:

```bash
python evals/run_eval.py
```

The evaluation suite currently contains **8 verification cases**.

### Latest Evaluation Run

| Metric         | Result            |
| -------------- | ----------------- |
| Date           | September 3, 2026 |
| Prompt Version | `enrich-v1.md`    |
| Test Cases     | 8                 |
| Passed         | 8                 |
| Failed         | 0                 |
| Pass Rate      | **100.0%**        |
| Status         | ✅ Passed          |

---

# 📝 Prompt Versioning

LLM instructions are maintained separately from application code.

Current prompt:

```text
prompts/enrich-v1.md
```

This allows prompt changes to be tracked independently and makes evaluation results easier to reproduce against specific prompt versions.

---

# 🐳 Useful Docker Commands

### Build and start

```bash
docker compose up --build
```

### Build and start in detached mode

```bash
docker compose up -d --build
```

### View running containers

```bash
docker compose ps
```

### Follow application logs

```bash
docker compose logs -f
```

### Stop the stack

```bash
docker compose down
```

### Stop the stack and remove volumes

```bash
docker compose down -v
```

> ⚠️ Removing volumes deletes persistent PostgreSQL data stored in Docker volumes.

---

# 🔄 System Overview

The workspace brings together three backend components:

```text
                  ┌─────────────────────┐
                  │    Polite Scraper   │
                  │   Books to Scrape   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Book Records      │
                  │ Title + Description │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  LLM Enrichment     │
                  │ Classification +    │
                  │ Themes + Summary    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Structured Output   │
                  │ Pydantic Validation │
                  └─────────────────────┘


        ┌───────────────────────────────┐
        │        Task API               │
        │                               │
        │ FastAPI ──► PostgreSQL        │
        └───────────────────────────────┘
```

---

# 🎯 Engineering Concepts Demonstrated

This workspace demonstrates practical backend engineering concepts including:

* REST API design
* CRUD operations
* FastAPI application architecture
* Asynchronous LLM API integration
* Structured LLM output validation
* Pydantic v2 schemas
* Retry and exponential backoff strategies
* Defensive parsing
* Failure isolation and quarantine logging
* Automated LLM evaluation
* Prompt versioning
* PostgreSQL integration
* SQLAlchemy
* Docker containerization
* Docker Compose orchestration
* Environment-based configuration
* Web scraping
* HTML parsing
* Rate limiting
* Local caching
* Structured data extraction

---

# 📌 Project Status

This repository serves as a progressively developed **backend engineering workspace**, combining traditional backend systems with AI-powered data enrichment.

The current workspace includes:

* ✅ Containerized FastAPI Task API
* ✅ PostgreSQL integration
* ✅ Async LLM enrichment service
* ✅ Structured Pydantic output validation
* ✅ Retry and fallback handling
* ✅ Quarantine logging
* ✅ Versioned enrichment prompts
* ✅ Automated evaluation suite
* ✅ Polite web scraping pipeline
* ✅ Local scraping cache and structured outputs

---
