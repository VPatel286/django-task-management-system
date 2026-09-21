# Django Task Management System

![CI](https://github.com/VPatel286/django-task-management-system/actions/workflows/ci.yml/badge.svg)

A full-stack task management application built with **Django REST Framework** and **React**.

The application provides secure JWT-based authentication, task management, categories, tags, filtering, searching, ordering, pagination, background task processing, automated testing, PostgreSQL persistence, Redis/Celery integration, Docker containerization, and GitHub Actions CI.

## Project Overview

This project was built as a production-style portfolio application to demonstrate practical experience with:

* REST API development
* JWT authentication and authorization
* Object-level permissions and task ownership
* Relational database design with PostgreSQL
* Service-layer architecture
* API filtering, searching, ordering, and pagination
* Redis and Celery background processing
* Automated testing with pytest
* Docker and Docker Compose
* React frontend development
* CI automation with GitHub Actions
* API documentation with OpenAPI/Swagger
* Security-focused Django configuration

The application follows a **Django REST API + React frontend** architecture, with PostgreSQL as the primary database and Redis used for asynchronous background processing.

## Features

### Authentication & User Management

* User registration with password validation
* JWT-based authentication
* Access and refresh token workflow
* Token refresh support
* Authenticated user profile endpoint
* Password change functionality
* Password validation using Django's built-in validators
* Protected API endpoints

### Task Management

* Create, retrieve, update, and delete tasks
* Task ownership and user-level data isolation
* Object-level permissions
* Task priorities:

  * Low
  * Medium
  * High
  * Urgent
* Task statuses:

  * To Do
  * In Progress
  * Completed
  * Cancelled
* Task descriptions
* Task completion tracking
* Task creation and update timestamps
* Optional task categories
* Multiple tags per task

### API Features

* RESTful API architecture
* URL-based API versioning
* Filtering
* Search
* Ordering
* Pagination
* Validation and structured error responses
* Custom exception handling
* OpenAPI schema generation
* Swagger API documentation
* JWT Bearer authentication in Swagger

### Database & Performance

* PostgreSQL database
* Foreign-key relationships
* Many-to-many relationships
* Database indexes
* Query optimization using `select_related`
* Query optimization using `prefetch_related`
* PostgreSQL query analysis with `EXPLAIN ANALYZE`
* Database transactions and rollback handling

### Background Processing

* Redis message broker
* Celery background workers
* Asynchronous task processing
* Transaction-safe task dispatch using `transaction.on_commit`
* Celery logging
* Automatic task retry handling

### Security

* Environment-based configuration
* Secrets excluded from Git
* CORS configuration
* Secure cookies in production
* HTTPS redirect configuration
* HTTP Strict Transport Security (HSTS)
* Authenticated API access
* Object-level authorization
* Request throttling

### Testing

* Automated API tests using pytest
* Django test database
* Authentication and authorization tests
* Task CRUD tests
* Ownership and permission tests
* Validation tests
* Service-layer tests
* Password management tests
* Mocking of background tasks
* Test coverage support

### Frontend

* React-based user interface
* Vite development environment
* Axios API integration
* Login and registration
* JWT token handling
* Task creation and editing
* Task deletion
* Category management
* Tags
* Search and filtering
* Loading and error states
* Responsive UI

### DevOps & Infrastructure

* Dockerized backend
* Dockerized React frontend
* PostgreSQL container
* Redis container
* Celery worker container
* Nginx for serving the production React build
* Docker Compose orchestration
* GitHub Actions CI pipeline
* Automated database migrations in CI
* Automated backend test execution in CI


## Tech Stack

| Layer                 | Technology                            |
| --------------------- | ------------------------------------- |
| Backend               | Python, Django, Django REST Framework |
| Authentication        | JWT, Simple JWT                       |
| Frontend              | React, Vite, JavaScript               |
| API Client            | Axios                                 |
| Database              | PostgreSQL                            |
| ORM                   | Django ORM                            |
| Background Processing | Celery                                |
| Message Broker        | Redis                                 |
| API Documentation     | OpenAPI, Swagger UI, drf-spectacular  |
| Testing               | pytest, pytest-django, pytest-cov     |
| Containerization      | Docker, Docker Compose                |
| Web Server            | Nginx                                 |
| CI/CD                 | GitHub Actions                        |
| Version Control       | Git, GitHub                           |

## Architecture

The application uses a full-stack architecture where the React frontend communicates with the Django REST API.

```text
┌──────────────────────┐
│      React UI        │
│      Vite + Axios    │
└──────────┬───────────┘
           │
           │ HTTP / JSON
           │ JWT Authentication
           ▼
┌──────────────────────┐
│   Django REST API    │
│   Django REST        │
│   Framework          │
└───────┬────────┬─────┘
        │        │
        │        │ Background Jobs
        │        ▼
        │   ┌──────────────┐
        │   │    Celery    │
        │   │    Worker    │
        │
```

## Project Structure

```text
django-task-management-system/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── wsgi.py
│   └── asgi.py
│
├── task_api/
│   ├── migrations/
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   ├── test_categories.py
│   │   ├── test_tags.py
│   │   └── ...
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── services.py
│   ├── tasks.py
│   ├── exceptions.py
│   ├── urls.py
│   └── admin.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

### Backend Responsibilities

| File / Directory          | Responsibility                                                                           |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| `config/settings.py`      | Django configuration, database, security, REST Framework, CORS, and environment settings |
| `config/urls.py`          | Root URL configuration, API versioning, authentication, and API documentation            |
| `config/celery.py`        | Celery application configuration                                                         |
| `task_api/models.py`      | Database models and relationships                                                        |
| `task_api/serializers.py` | API serialization and request validation                                                 |
| `task_api/views.py`       | API endpoints and request handling                                                       |
| `task_api/services.py`    | Task-related business logic                                                              |
| `task_api/permissions.py` | Custom authorization and object-level permissions                                        |
| `task_api/tasks.py`       | Celery background tasks                                                                  |
| `task_api/exceptions.py`  | Custom API exception handling                                                            |
| `task_api/tests/`         | Automated backend tests                                                                  |

### Frontend Responsibilities

The React application is responsible for:

* User registration and login
* JWT authentication handling
* Task management UI
* Category and tag management
* Searching and filtering
* API communication through Axios
* Loading and error states
* Responsive user interface

### Infrastructure

Docker Compose orchestrates the main application services:

```text
React + Nginx
      │
      ▼
Django API
   │       │
   ▼       ▼
PostgreSQL Redis
             │
             ▼
           Celery
```

## API Endpoints

The API uses URL-based versioning. The current API version is `v1`.

### Authentication

| Method | Endpoint                   | Description                      | Authentication |
| ------ | -------------------------- | -------------------------------- | -------------- |
| `POST` | `/api/register/`           | Register a new user              | Public         |
| `POST` | `/api/token/`              | Obtain access and refresh tokens | Public         |
| `POST` | `/api/token/refresh/`      | Refresh an access token          | Public         |
| `GET`  | `/api/v1/me/`              | Get authenticated user profile   | JWT            |
| `POST` | `/api/v1/change-password/` | Change account password          | JWT            |

### Tasks

| Method   | Endpoint              | Description             | Authentication |
| -------- | --------------------- | ----------------------- | -------------- |
| `GET`    | `/api/v1/tasks/`      | List user's tasks       | JWT            |
| `POST`   | `/api/v1/tasks/`      | Create a task           | JWT            |
| `GET`    | `/api/v1/tasks/{id}/` | Retrieve a task         | JWT + Owner    |
| `PUT`    | `/api/v1/tasks/{id}/` | Update a task           | JWT + Owner    |
| `PATCH`  | `/api/v1/tasks/{id}/` | Partially update a task | JWT + Owner    |
| `DELETE` | `/api/v1/tasks/{id}/` | Delete a task           | JWT + Owner    |

### Categories

| Method   | Endpoint                   | Description                 | Authentication |
| -------- | -------------------------- | --------------------------- | -------------- |
| `GET`    | `/api/v1/categories/`      | List categories             | JWT            |
| `POST`   | `/api/v1/categories/`      | Create a category           | JWT            |
| `GET`    | `/api/v1/categories/{id}/` | Retrieve a category         | JWT            |
| `PUT`    | `/api/v1/categories/{id}/` | Update a category           | JWT            |
| `PATCH`  | `/api/v1/categories/{id}/` | Partially update a category | JWT            |
| `DELETE` | `/api/v1/categories/{id}/` | Delete a category           | JWT            |

### Tags

| Method   | Endpoint             | Description            | Authentication |
| -------- | -------------------- | ---------------------- | -------------- |
| `GET`    | `/api/v1/tags/`      | List tags              | JWT            |
| `POST`   | `/api/v1/tags/`      | Create a tag           | JWT            |
| `GET`    | `/api/v1/tags/{id}/` | Retrieve a tag         | JWT            |
| `PUT`    | `/api/v1/tags/{id}/` | Update a tag           | JWT            |
| `PATCH`  | `/api/v1/tags/{id}/` | Partially update a tag | JWT            |
| `DELETE` | `/api/v1/tags/{id}/` | Delete a tag           | JWT            |

### API Documentation

| Method | Endpoint       | Description               |
| ------ | -------------- | ------------------------- |
| `GET`  | `/api/schema/` | OpenAPI schema            |
| `GET`  | `/api/docs/`   | Swagger API documentation |

### Task Query Parameters

The task endpoint supports filtering, searching, ordering, and pagination.

#### Filtering

```text
GET /api/v1/tasks/?status=IN_PROGRESS
GET /api/v1/tasks/?completed=true
```

#### Searching

```text
GET /api/v1/tasks/?search=django
```

Search is performed against task titles and descriptions.

#### Ordering

```text
GET /api/v1/tasks/?ordering=title
GET /api/v1/tasks/?ordering=-created_at
```

A leading `-` sorts the results in descending order.

#### Pagination

```text
GET /api/v1/tasks/?page=2
```

The API returns paginated results when the result set exceeds the

## Authentication & Authorization

The application uses **JWT (JSON Web Token) authentication** to secure API endpoints.

### Authentication Flow

```text
User
 │
 │ Login
 ▼
POST /api/token/
 │
 │ Access + Refresh Token
 ▼
React Frontend
 │
 │ Authorization: Bearer <access_token>
 ▼
Django REST API
 │
 │ JWT Validation
 ▼
Authenticated Request
```

### Access and Refresh Tokens

The application uses two JWT tokens:

* **Access token** — Used to authenticate API requests.
* **Refresh token** — Used to obtain a new access token after the access token expires.

The configured token lifetimes are:

| Token         | Lifetime   |
| ------------- | ---------- |
| Access Token  | 30 minutes |
| Refresh Token | 7 days     |

### Protected Endpoints

Authenticated endpoints require a valid JWT access token.

Requests include:

```http
Authorization: Bearer <access_token>
```

Django REST Framework validates the token before allowing access to protected resources.

### User Registration

New users can register through the registration endpoint.

During registration:

1. Username is validated.
2. Password validation rules are applied.
3. The password is securely hashed using Django's authentication system.
4. A new user account is created.

Passwords are never stored as plain text.

### Task Ownership

Every task belongs to the user who created it.

The `Task` model uses a foreign-key relationship:

```text
User
 │
 └───< Task
```

When retrieving the task list, the API only returns tasks belonging to the authenticated user.

This provides **user-level data isolation**.

### Object-Level Permissions

Individual task operations use a custom `IsTaskOwner` permission.

For example:

```text
User A
 ├── Task 1
 └── Task 2

User B
 ├── Task 3
 └── Task 4
```

User A can access Task 1 and Task 2, but cannot modify or delete User B's tasks.

This authorization is enforced on the server rather than relying on frontend restrictions.

### Password Management

Authenticated users can change their password through the password-change endpoint.

The process validates:

1. Current password
2. New password
3. Django password validation rules

The password is then securely updated using Django's password hashing mechanism.

### Security Controls

The API also includes:

* Request throttling
* CORS configuration
* Environment-based secrets
* Secure production cookie configuration
* HTTPS redirect configuration
* HSTS configuration
* Object-level authorization
* Protected API endpoints
* Database-level constraints


## Authentication & Authorization

The application uses **JWT (JSON Web Token) authentication** to secure API endpoints.

### Authentication Flow

```text
User
 │
 │ Login
 ▼
POST /api/token/
 │
 │ Access + Refresh Token
 ▼
React Frontend
 │
 │ Authorization: Bearer <access_token>
 ▼
Django REST API
 │
 │ JWT Validation
 ▼
Authenticated Request
```

### Access and Refresh Tokens

The application uses two JWT tokens:

* **Access token** — Used to authenticate API requests.
* **Refresh token** — Used to obtain a new access token after the access token expires.

The configured token lifetimes are:

| Token         | Lifetime   |
| ------------- | ---------- |
| Access Token  | 30 minutes |
| Refresh Token | 7 days     |

### Protected Endpoints

Authenticated endpoints require a valid JWT access token.

Requests include:

```http
Authorization: Bearer <access_token>
```

Django REST Framework validates the token before allowing access to protected resources.

### User Registration

New users can register through the registration endpoint.

During registration:

1. Username is validated.
2. Password validation rules are applied.
3. The password is securely hashed using Django's authentication system.
4. A new user account is created.

Passwords are never stored as plain text.

### Task Ownership

Every task belongs to the user who created it.

The `Task` model uses a foreign-key relationship:

```text
User
 │
 └───< Task
```

When retrieving the task list, the API only returns tasks belonging to the authenticated user.

This provides **user-level data isolation**.

### Object-Level Permissions

Individual task operations use a custom `IsTaskOwner` permission.

For example:

```text
User A
 ├── Task 1
 └── Task 2

User B
 ├── Task 3
 └── Task 4
```

User A can access Task 1 and Task 2, but cannot modify or delete User B's tasks.

This authorization is enforced on the server rather than relying on frontend restrictions.

### Password Management

Authenticated users can change their password through the password-change endpoint.

The process validates:

1. Current password
2. New password
3. Django password validation rules

The password is then securely updated using Django's password hashing mechanism.

### Security Controls

The API also includes:

* Request throttling
* CORS configuration
* Environment-based secrets
* Secure production cookie configuration
* HTTPS redirect configuration
* HSTS configuration
* Object-level authorization
* Protected API endpoints
* Database-level constraints

## Database Design

The application uses **PostgreSQL** as its primary relational database.

The database is designed around users, tasks, categories, and tags.

### Entity Relationships

```text id="p8r4vz"
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       │ 1 : Many
       ▼
┌──────────────┐
│     Task     │
└───┬──────┬───┘
    │      │
    │      │ Many : Many
    │      ▼
    │   ┌──────────────┐
    │   │     Tag      │
    │   └──────────────┘
    │
    │ Many : 1
    ▼
┌──────────────┐
│   Category   │
└──────────────┘
```

### User → Task

A user can own multiple tasks.

```text
User 1 ────────< Task
```

Each task has exactly one owner.

This relationship is implemented using a Django `ForeignKey`.

### Task → Category

A task can optionally belong to a category.

```text
Category 1 ────────< Task
```

The category relationship allows tasks to be grouped without requiring every task to have a category.

The relationship uses `SET_NULL`, so deleting a category does not delete its associated tasks.

### Task ↔ Tag

A task can have multiple tags, and a tag can belong to multiple tasks.

```text
Task >──────< Tag
```

This is implemented using a Django `ManyToManyField`.

For example:

```text id="w7s9za"
Task: Learn Django REST Framework

Tags:
- Django
- REST API
- Backend
- Python
```

### Database Constraints

The application uses database-level constraints to help maintain data integrity.

Examples include:

* Unique usernames through Django's authentication model
* Unique category names
* Unique tag names
* Valid task priority values
* Foreign-key relationships
* Many-to-many relationship integrity

Task priorities are restricted to:

```text id="l5qk3n"
LOW
MEDIUM
HIGH
URGENT
```

### Indexing

Indexes are used for fields that are frequently queried.

For example, the task `status` field is indexed to improve filtering performance.

```python
status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.TODO,
    db_index=True,
)
```

### Query Optimization

The API uses Django ORM optimization techniques to reduce unnecessary database queries.

#### `select_related`

Used for foreign-key relationships such as:

```text id="x2j9hz"
Task → Category
```

This allows related category data to be retrieved efficiently using SQL joins.

#### `prefetch_related`

Used for many-to-many relationships such as:

```text id="c7m3rp"
Task ↔ Tag
```

This allows related tags to be fetched efficiently without executing a separate query for every task.

### Query Analysis

PostgreSQL's `EXPLAIN ANALYZE` was used to inspect query execution and verify database performance.

This helped identify how PostgreSQL executes queries and whether indexes are being used effectively.

### Transaction Management

Database operations that require consistency are handled using Django transactions.

The application also uses `transaction.on_commit()` when dispatching background Celery jobs so that asynchronous processing only starts after the database transaction has successfully committed.

## Background Processing & Asynchronous Tasks

The application uses **Redis** and **Celery** to process background work asynchronously.

This prevents non-critical processing from blocking the main API request.

### Architecture

```text id="j9q6mk"
Django API
    │
    │ Create Task
    ▼
PostgreSQL
    │
    │ Transaction committed
    ▼
Redis Broker
    │
    │ Queue message
    ▼
Celery Worker
    │
    │ Process background job
    ▼
Task Result / Logging
```

### Redis

Redis is used as the **message broker** between Django and Celery.

It provides a fast in-memory queue where background jobs can wait until a Celery worker processes them.

### Celery

Celery handles asynchronous background execution.

The application includes a task that processes newly created tasks:

```python
@shared_task(bind=True, max_retries=3)
def process_task(self, task_id):
    ...
```

The task receives the database task ID rather than the complete Django model object.

This keeps the queued message lightweight and allows the worker to retrieve the latest database state when required.

### Transaction-Safe Task Dispatch

The application uses Django's `transaction.on_commit()` when dispatching Celery jobs.

```python
transaction.on_commit(
    lambda: process_task.delay(task.id)
)
```

This is important because the Celery job should not start before the database transaction has successfully committed.

Without `on_commit()`, a worker could potentially receive the task while the corresponding database transaction is still pending or could fail entirely.

The workflow is therefore:

```text id="7q3jvk"
Create Task
    │
    ▼
Database Transaction
    │
    ├── Rollback ──► Celery job is NOT dispatched
    │
    └── Commit
         │
         ▼
    Celery job dispatched
         │
         ▼
    Redis
         │
         ▼
    Celery Worker
```

### Retry Handling

Celery tasks are configured with retry support.

The current background task allows up to three retries:

```python
@shared_task(bind=True, max_retries=3)
```

If an unexpected exception occurs, the task logs the error and schedules a retry.

```python
raise self.retry(
    exc=exc,
    countdown=5
)
```

This provides basic resilience for transient background-processing failures.

### Logging

Celery tasks use Python's standard logging framework.

The worker records:

* Task ID
* Processing status
* Exceptions
* Retry information

This makes background processing easier to monitor and troubleshoot.

### Why Asynchronous Processing?

Moving background work outside the HTTP request improves the architecture by separating:

* **Request/response operations** handled by Django
* **Long-running or non-critical operations** handled by Celery

This allows the API to respond without waiting for every background operation to finish.

### Docker Services

The development environment runs the asynchronous infrastructure as separate Docker services:

```text
┌─────────────────┐
│   Django Web    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      Redis      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Celery Worker   │
└─────────────────┘
```

This separation makes the application architecture closer to how asynchronous workloads can be deployed in a production environment.


## Testing & Code Quality

The backend includes an automated test suite using **pytest**, **pytest-django**, and **pytest-cov**.

The goal is to verify API functionality, authentication, authorization, validation, business logic, and database behavior.

### Test Coverage

The test suite currently contains **43 automated tests** covering areas such as:

* User registration
* JWT authentication
* Token refresh
* User profile
* Password changes
* Task creation
* Task retrieval
* Task updates
* Task deletion
* Task validation
* Task ownership
* Object-level permissions
* Category operations
* Tag operations
* Filtering
* Searching
* Ordering
* Pagination
* Service-layer logic
* Background task integration
* Error handling

### Running Tests

Tests can be executed inside the Dockerized Django service:

```bash
docker compose exec web pytest -v
```

Example result:

```text
43 passed
```

### Test Isolation

Tests use Django's test database functionality so that test data remains isolated from the application's development database.

Reusable pytest fixtures are used to create common test objects such as:

* Test users
* Authenticated API clients
* Tasks
* Categories
* Tags

This reduces duplication across individual tests.

### Authentication Testing

Authentication-related tests verify that protected endpoints reject unauthenticated requests.

For example:

```text
Unauthenticated request
        │
        ▼
Protected endpoint
        │
        ▼
HTTP 401 Unauthorized
```

Authenticated requests are tested using JWT credentials.

### Authorization Testing

The test suite verifies that users cannot access or modify another user's tasks.

For example:

```text
User A
 │
 ├── Task 1 ✓
 └── Task 2 ✓

User B
 │
 ├── Task 1 ✗
 └── Task 2 ✗
```

This validates both user-level data isolation and object-level permissions.

### Service-Layer Testing

Business logic implemented in `services.py` is tested independently from the API views.

This helps verify task creation, updates, tag assignment, and deletion behavior without relying exclusively on HTTP-level tests.

### Mocking Background Tasks

Celery operations can be mocked during tests when the purpose of the test is to verify API behavior rather than execute an actual background worker.

This keeps tests:

* Faster
* Deterministic
* Easier to debug
* Independent of external background workers

### Code Coverage

The project includes `pytest-cov` for measuring test coverage.

Coverage can be generated with:

```bash
pytest --cov=task_api
```

An HTML coverage report can also be generated:

```bash
pytest --cov=task_api --cov-report=html
```

### Continuous Integration

GitHub Actions automatically runs the backend test suite whenever changes are pushed to the repository or submitted through a pull request.

The CI pipeline:

1. Checks out the repository.
2. Sets up Python.
3. Starts PostgreSQL.
4. Starts Redis.
5. Installs Python dependencies.
6. Runs Django migrations.
7. Executes the pytest test suite.

```text
Git Push / Pull Request
          │
          ▼
    GitHub Actions
          │
    ┌─────┴─────┐
    ▼           ▼
PostgreSQL     Redis
    │           │
    └─────┬─────┘
          ▼
    Django Migrations
          │
          ▼
       pytest
          │
     ┌────┴────┐
     ▼         ▼
   Passed    Failed
```

A passing CI pipeline provides an automated verification step before changes are considered ready to merge.

### Code Quality Approach

The project follows several practices to keep the code maintainable:

* Separation of API views and business logic
* Reusable serializers
* Custom permission classes
* Reusable pytest fixtures
* Environment-based configuration
* Database constraints
* Query optimization
* Automated testing
* CI validation
* Clear project structure


## Docker & Local Development

The application is fully containerized using **Docker** and **Docker Compose**.

The development environment consists of separate services for the backend, frontend, database, Redis, and Celery worker.

### Docker Services

| Service    | Purpose                           | Port     |
| ---------- | --------------------------------- | -------- |
| `web`      | Django REST API                   | `8000`   |
| `frontend` | React application served by Nginx | `5173`   |
| `db`       | PostgreSQL database               | `5432`   |
| `redis`    | Celery message broker             | `6379`   |
| `celery`   | Background task worker            | Internal |

### Service Architecture

```text
                    ┌─────────────────┐
                    │ React + Nginx   │
                    │   Port 5173     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Django API    │
                    │   Port 8000     │
                    └──────┬─────┬────┘
                           │     │
              ┌────────────┘     └────────────┐
              ▼                               ▼
      ┌─────────────────┐             ┌─────────────────┐
      │   PostgreSQL    │             │      Redis      │
      │    Port 5432    │             │    Port 6379    │
      └─────────────────┘             └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Celery Worker   │
                                      └─────────────────┘
```

### Environment Configuration

Sensitive configuration is stored in environment variables rather than committed to Git.

Examples include:

* Django secret key
* Database credentials
* Database host and port
* Redis connection settings
* Celery broker configuration
* Debug configuration

The `.env` file is excluded from Git using `.gitignore`.

A safe environment template can be provided separately for new developers.

### Start the Application

After cloning the repository and configuring the environment variables, start all services with:

```bash
docker compose up --build
```

Docker Compose starts the required services and builds the application containers.

### Run in the Background

To start the services in detached mode:

```bash
docker compose up -d --build
```

Check running containers with:

```bash
docker compose ps
```

### Stop the Application

```bash
docker compose down
```

To stop the application and remove the containers while keeping the PostgreSQL volume:

```bash
docker compose down
```

The PostgreSQL data is stored in a Docker volume so that restarting the containers does not automatically remove the database.

### Run Django Commands

Django management commands can be executed inside the backend container.

For example, to apply migrations:

```bash
docker compose exec web python manage.py migrate
```

To create a Django superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

To run the automated tests:

```bash
docker compose exec web pytest -v
```

### View Celery Logs

Celery worker logs can be viewed with:

```bash
docker compose logs -f celery
```

### View Backend Logs

```bash
docker compose logs -f web
```

### Rebuild After Backend Changes

The backend source code is included in the Docker image.

After backend dependency or source changes, rebuild the backend service:

```bash
docker compose up -d --build web
```

### Frontend Production Build

The React frontend uses a multi-stage Docker build.

The first stage:

```text
Node.js
   │
   ▼
npm ci
   │
   ▼
npm run build
   │
   ▼
React production files
```

The second stage uses Nginx to serve the generated production files:

```text
React Build
     │
     ▼
   Nginx
     │
     ▼
Browser
```

This keeps the final frontend image focused on serving the compiled application rather than including the Node.js build environment.

### Health Checks

Docker Compose uses health checks for PostgreSQL and Redis.

The backend and Celery services depend on these services becoming healthy before starting.

This helps prevent application containers from starting before their required infrastructure is ready.

## How to Run the Project

### Prerequisites

Make sure the following are installed:

* Git
* Docker Desktop
* Docker Compose
* Node.js (only required if running the frontend outside Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/VPatel286/django-task-management-system.git
cd django-task-management-system
```

### 2. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key

DB_NAME=task_api_db
DB_USER=task_api_user
DB_PASSWORD=your-database-password
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

> Never commit the `.env` file or real secrets to GitHub.

### 3. Build and Start the Application

Run:

```bash
docker compose up -d --build
```

Verify that the services are running:

```bash
docker compose ps
```

The expected services are:

```text
web
frontend
db
redis
celery
```

### 4. Run Database Migrations

Apply Django migrations:

```bash
docker compose exec web python manage.py migrate
```

### 5. Create an Admin User

Create a Django administrator account:

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to configure the account.

### 6. Run the Test Suite

Run the automated tests:

```bash
docker compose exec web pytest -v
```

The current test suite contains 43 automated tests.

### 7. Access the Application

Once the containers are running:

| Component        | Address                             |
| ---------------- | ----------------------------------- |
| React Frontend   | `http://localhost:5173`             |
| Django API       | `http://localhost:8000`             |
| Django Admin     | `http://localhost:8000/admin/`      |
| Swagger API Docs | `http://localhost:8000/api/docs/`   |
| OpenAPI Schema   | `http://localhost:8000/api/schema/` |

### 8. Stop the Application

To stop the containers:

```bash
docker compose down
```

To stop the containers and remove the PostgreSQL data volume:

```bash
docker compose down -v
```

> Use `docker compose down -v` carefully because it deletes the PostgreSQL Docker volume and therefore removes the database data stored in that volume.

### Troubleshooting

#### Check Container Status

```bash
docker compose ps
```

#### View Backend Logs

```bash
docker compose logs -f web
```

#### View Celery Logs

```bash
docker compose logs -f celery
```

#### View PostgreSQL Logs

```bash
docker compose logs -f db
```

#### Restart the Application

```bash
docker compose down
docker compose up -d --build
```

#### Rebuild a Specific Service

Backend:

```bash
docker compose up -d --build web
```

Frontend:

```bash
docker compose up -d --build frontend
```

Celery:

```bash
docker compose up -d --build celery
```

## Continuous Integration

The project uses **GitHub Actions** to automatically validate changes pushed to the repository.

The CI workflow runs for:

* Pushes to `main`
* Pull requests targeting `main`

### CI Pipeline

```text id="c0q7nh"
Git Push / Pull Request
          │
          ▼
    GitHub Actions
          │
          ▼
   Checkout Repository
          │
          ▼
    Setup Python 3.12
          │
          ▼
   Install Dependencies
          │
          ▼
 ┌─────────────────────┐
 │ PostgreSQL Service  │
 │      +              │
 │ Redis Service       │
 └──────────┬──────────┘
            │
            ▼
     Django Migrations
            │
            ▼
       pytest -v
            │
       ┌────┴────┐
       ▼         ▼
     PASS       FAIL
```

### Services Used in CI

The GitHub Actions environment starts:

* PostgreSQL 18
* Redis 7

This allows the test suite to run against infrastructure similar to the Docker development environment.

### CI Steps

The workflow performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs project dependencies.
4. Starts PostgreSQL.
5. Starts Redis.
6. Runs Django database migrations.
7. Executes the complete pytest test suite.

### Environment Isolation

CI uses dedicated test credentials and environment variables.

Real development or production secrets are not stored in the repository.

### Current CI Status

The CI workflow has been successfully executed against the `main` branch.

A passing workflow confirms that:

* Dependencies can be installed successfully.
* PostgreSQL connectivity works.
* Redis connectivity works.
* Django migrations succeed.
* The automated test suite passes.

The repository also includes a CI status badge at the top of this README.


## Screenshots / Demo

The application provides a responsive React interface for managing tasks through the Django REST API.

### Login

The login page allows users to authenticate using their account credentials and obtain JWT tokens.

<!-- Add login screenshot here -->

### Task Dashboard

The dashboard provides an overview of the user's tasks, including task status, priority, categories, and tags.

<!-- Add dashboard screenshot here -->

### Create / Edit Task

Users can create and update tasks with:

* Title
* Description
* Status
* Priority
* Category
* Tags

<!-- Add task form screenshot here -->

### Search & Filtering

The task interface supports searching, filtering, and ordering to help users find specific tasks efficiently.

<!-- Add search/filter screenshot here -->

### API Documentation

The backend provides interactive Swagger documentation for exploring and testing the REST API.

<!-- Add Swagger screenshot here -->

### Docker Environment

The complete application runs through Docker Compose with separate services for:

* React + Nginx
* Django REST API
* PostgreSQL
* Redis
* Celery

<!-- Add Docker services screenshot here -->


## Future Improvements

The current application provides a complete full-stack task management workflow. Possible future enhancements include:

### Application Features

* Email notifications for task events
* Task due dates and reminders
* Recurring tasks
* File attachments
* Activity history and audit logs
* Advanced dashboard analytics
* User-specific task preferences

### Backend Improvements

* More advanced Celery workflows
* Scheduled background jobs
* Redis caching for frequently accessed data
* Advanced API rate limiting
* Additional database performance tuning
* Expanded API integration tests

### Frontend Improvements

* Improved dashboard visualizations
* Drag-and-drop task management
* Dark mode
* Advanced task filtering
* Real-time updates using WebSockets
* Improved accessibility support

### DevOps & Deployment

* Production deployment to a cloud platform
* Automated deployment pipeline
* Production monitoring and logging
* Container image publishing
* Infrastructure-as-code configuration
* Application health and performance monitoring

These improvements can be introduced incrementally while keeping the existing API architecture and database design maintainable.


## Key Technical Concepts Demonstrated

This project demonstrates practical experience with the following software engineering concepts:

### Backend Development

* RESTful API design
* Django REST Framework
* Serializer-based validation
* Generic API views
* JWT authentication
* Access and refresh token workflows
* Object-level authorization
* Custom permission classes
* API versioning
* Filtering, searching, ordering, and pagination
* Structured API error handling

### Software Architecture

* Separation of API views and business logic
* Service-layer architecture
* Reusable components
* Separation of concerns
* Dependency-aware application design
* Transaction management
* Asynchronous processing

### Database Engineering

* Relational database modeling
* Foreign-key relationships
* Many-to-many relationships
* Database constraints
* Database indexes
* Query optimization
* `select_related`
* `prefetch_related`
* PostgreSQL query analysis
* `EXPLAIN ANALYZE`

### Asynchronous Processing

* Redis message brokering
* Celery workers
* Background task processing
* Retry handling
* Task logging
* Transaction-safe task dispatching
* `transaction.on_commit()`

### Testing

* Unit and API testing
* pytest
* pytest-django
* Test fixtures
* Authentication testing
* Authorization testing
* Ownership testing
* Mocking
* Code coverage
* Test database isolation

### Frontend Development

* React component architecture
* Vite
* Axios
* JWT client-side handling
* API integration
* Form handling
* Loading and error states
* Search and filtering
* Responsive UI development

### DevOps

* Docker
* Docker Compose
* Multi-stage Docker builds
* Nginx
* PostgreSQL containers
* Redis containers
* Celery workers
* Environment-based configuration
* GitHub Actions
* Automated CI testing

## License

This project is intended for educational and portfolio purposes.

## Author

**Vraj Patel**

Full-Stack Software Developer focused on backend development, REST APIs, Java/Python, databases, and cloud-ready application architecture.

### Technologies & Areas of Interest

* Java
* Python
* Django REST Framework
* React
* REST APIs
* PostgreSQL
* Redis
* Celery
* Docker
* GitHub Actions
* Software Architecture
* Backend Development


