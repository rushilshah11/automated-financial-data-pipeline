# 📈 Automated Financial Data Pipeline

The Automated Financial Data Pipeline is a full-stack system designed to automatically collect, process, and deliver personalized financial updates to users. The project focuses on building reliable backend automation, ensuring data flows seamlessly from collection (via financial APIs) to processing (calculating insights) and finally to delivery (personalized user updates). 

A lightweight React web interface is included to visualize the results, test features, and understand how the user-facing side connects to the backend. It also showcases modern software engineering principles, cloud deployment readiness, and end-to-end data orchestration.

---

## Core Technologies and Ecosystem

| Category | Technology | Purpose & Key Implementation Details |
|----------|------------|--------------------------------------|
| **Backend API** | FastAPI (Python 3.11) | High-performance, asynchronous ASGI web framework for the REST API. Handles user authentication and subscription management. |
| **Data Layer** | PostgreSQL | Primary relational database for user and subscription data. Managed via Docker for local development, designed for cloud solutions like AWS RDS or Supabase. |
| **ORM & Models** | SQLAlchemy & Pydantic | SQLAlchemy for declarative data modeling (`app/db/models/`). Pydantic for input/output schema validation (`app/db/schemas/`), enforcing data contracts. |
| **External Integrations** | Finnhub API | Third-party financial data provider for stock quotes and company profiles (`app/core/integrations/finnhub_client.py`). |
| **Cloud Services** | AWS SES & AWS S3 | SES dispatches daily updates. S3 stores pipeline execution logs (`app/core/integrations/s3_client.py`). |
| **Security/Auth** | JWT & Bcrypt | Stateless user authentication using JSON Web Tokens. Passwords hashed with bcrypt. |
| **DevOps & CI/CD** | Docker & GitHub Actions | Docker/Docker Compose for containerized development. GitHub Actions manages CI (`ci.yml`) and scheduled data orchestration (`daily_email.yml`). |
| **Frontend UI** | React | SPA client for user registration, login, and managing stock subscriptions. |

---

## 🧠 Software Engineering Principles & Thought Processes

### 1. Separation of Concerns (SoC) & Layered Architecture
The backend is strictly divided into layers:

- **Routers (`app/routers/`)**: Handles HTTP routing, request/response models, and dependency injection.  
- **Services (`app/service/`)**: Implements business logic (e.g., password hashing, subscription checks, ETL orchestration). Raises exceptions handled by routers.  
- **Repositories (`app/db/repository/`)**: Encapsulates database access logic (CRUD operations), keeping services decoupled from ORM.  
- **Models (`app/db/models/`)**: Defines database schema (tables/columns).  

---

### 2. Asynchronous Programming for Performance
- Uses `asyncio.to_thread` to prevent blocking during synchronous Finnhub API calls.  
- Database initialization (`create_tables`) runs asynchronously for smooth FastAPI startup.  

---

### 3. Data Integrity and Validation
- **Pydantic** validates request/response payloads and external data models (e.g., `StockQuoteOutput`, `CompanyProfileOutput`).  
- Database interactions use **SQLAlchemy Sessions** via FastAPI dependencies (`get_db`), ensuring atomic transactions.  

---

## 🚀 End-to-End Data Pipeline & Orchestration

### ETL Flow (`app/service/email_service.py`)
- **Extract**: Retrieves all unique subscribed tickers from PostgreSQL.  
- **Concurrent Extract/Transform**: Fetches stock quotes and company profiles in parallel using `asyncio.gather`.  
- **Load/Distribute**: Iterates through subscribed users, filters relevant data, and sends personalized emails via AWS SES.  

### Orchestration and Observability
- **Scheduling**: GitHub Actions workflow (`.github/workflows/daily_email.yml`) orchestrates daily dispatch.  
- **Logging**: Pipeline summary logs uploaded to AWS S3 for auditing and debugging.  

---

## ✅ Good Habits, Security, and Quality Assurance

### Continuous Integration & Testing
- **Pytest**: Integration tests cover user registration, login, and subscription CRUD.  
- **GitHub Actions CI**: Runs tests on each push/PR with a temporary PostgreSQL service.  
- **Test Strategy**: FastAPI TestClient ensures full stack validation, including DB interactions.  

### Environment and Deployment
- **Containerization**: Docker defines isolated environments for API and ETL scripts.  
- **Configuration**: Environment variables managed via dotenv; production secrets stored in GitHub Secrets or Render.  
- **CORS**: API restricts allowed frontend origins for security.  

### Logging and Documentation
- Structured logging with timestamps, levels, and module names (`app/core/logging_config.py`).  
- Internal Markdown documentation for core flows, JWT auth, and data models (`docs/`).  

---

## 🗺️ Repository Breakdown and Key Endpoints

| Path | Description | Key Files |
|------|------------|-----------|
| `app/` | Backend source code | `main.py`, `settings.py` |
| `app/core/` | Core functionality, DB config, security, external client wrappers | `database.py`, `security/`, `integrations/` |
| `app/service/` | Business logic & ETL | `user_service.py`, `subscription_service.py`, `email_service.py` |
| `app/db/` | Models, schemas, repositories | `models/`, `schemas/`, `repository/` |
| `app/routers/` | API endpoints | `auth.py`, `subscription.py` |
| `frontend/` | React SPA | `src/pages/`, `src/context/`, `src/api/` |
| `.github/` | GitHub Actions workflows | `workflows/ci.yml`, `workflows/daily_email.yml` |
| `tests/` | Integration test suite | `test_auth_flow.py`, `test_subscription_flow.py` |

### Key API Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/auth/register` | POST | Create new user | None |
| `/auth/login` | POST | Authenticate and return JWT | None |
| `/protected` | GET | Example JWT-protected route | Required |
| `/subscriptions/` | POST | Subscribe to a new ticker | Required |
| `/subscriptions/` | GET | List all subscriptions for the user | Required |
| `/subscriptions/{ticker}` | DELETE | Unsubscribe from a ticker | Required |

---

## 🧑‍💻 Author
**Rushil Shah**  
📫 [LinkedIn](https://linkedin.com/in/rushilshahh)
💼 Portfolio
