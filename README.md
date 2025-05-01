# automatic-enigma Backend

## Overview

This backend is a 12factor Django REST API with JWT authentication, SMS OTP, passwordless reset, Sentry/Twilio integration (via env), Metabase-ready, and full Docker support.  
All Python commands run inside a virtual environment, both locally and inside Docker.

---

## Local Development

1. **Setup Python venv and install dependencies:**
    ```
    cd backend
    make venv
    ```

2. **Common development commands:**
    ```
    make migrate           # Run Django migrations
    make run               # Start development server at http://localhost:8000
    make createsuperuser   # Create admin user
    make test              # Run tests
    make lint              # Lint code
    make cov               # Run tests with coverage
    make populate          # Populate test data
    make purge             # Purge all data
    make install-precommit # Install pre-commit hooks
    ```

3. **Environment management:**
    - Copy `.env.example` to `.env` and fill in your secrets.
    - All configuration is via environment variables.

---

## Virtual Environment in Docker

The Dockerfile creates a Python virtual environment at `/opt/venv` and sets the `PATH` so all commands run inside the venv by default.

**Dockerfile snippet:**
```
FROM python:3.11-slim

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```
- No global pip installs.
- All Python/Django commands (including in Docker) are executed in a virtual environment.

---

## Running in Docker

**Build the backend Docker image:**
```
make docker-build
```

**Run the backend container:**
```
make docker-run
```

**Open an interactive shell in the container:**
```
make docker-shell
```

---

## API & Admin

- **API Docs:**  
  - Redoc: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
  - Swagger: [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
- **Health Check:**  
  - [http://localhost:8000/health/](http://localhost:8000/health/)
- **Django Admin:**  
  - [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Metabase Analytics

- Metabase runs in Docker on port 3000 and connects to the SQLite file for analytics dashboards.

---

## Render.com Deployment

- Connect your repo to Render.com.
- Set environment variables in the Render dashboard.
- The Docker image uses the virtual environment for all operations.
- Expose port 8000.

---

## Notes

- All Python and Django commands are executed in a virtual environment, both locally and in Docker.
- The Makefile is idempotent and will auto-create the venv if missing.
- Test coverage must remain above 80% (CI will fail otherwise).
- For more details on project structure, see `docs/codebase.md`.

---

## Further Reading

- [Why use venv in Docker? (Hynek Schlawack)](https://hynek.me/articles/docker-virtualenv/)
- [Elegantly activating a virtualenv in a Dockerfile (PythonSpeed)](https://pythonspeed.com/articles/activate-virtualenv-dockerfile/)
- [Snyk: Mastering Python virtual environments](https://snyk.io/blog/mastering-python-virtual-environments/)
```

# automatic-enigma DevOps & Operations

## Overview

This section documents how to build, run, and manage the **automatic-enigma** project using Docker Compose, Nginx, and Metabase.  
It also provides Makefile commands for common DevOps and deployment tasks, and describes the updated project workflow.

---

## Docker & Docker Compose

### Project Services

- **backend**: Django/DRF app, running inside a venv, served by Gunicorn.
- **frontend**: Vue3/TypeScript/Tailwind SPA, built and served as static files.
- **nginx**: Reverse proxy for backend API and frontend SPA.
- **metabase**: Analytics dashboard, connects to the backend's SQLite DB.

---

## Docker Compose File (`docker-compose.yml`)

```
version: '3.8'

services:
  backend:
    build: ./backend
    env_file: ./backend/.env
    volumes:
      - ./backend:/app
      - ./backend/db.sqlite3:/app/db.sqlite3
    expose:
      - "8000"
    depends_on:
      - metabase

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
    command: ["npm", "run", "build"]

  nginx:
    build: ./infra/nginx
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend

  metabase:
    image: metabase/metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_FILE: /metabase.db
    volumes:
      - ./infra/metabase/metabase.db:/metabase.db
```

---

## Nginx Configuration (`infra/nginx/nginx.conf`)

```
server {
    listen 80;
    server_name _;

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Nginx Dockerfile (`infra/nginx/Dockerfile`)

```
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY ../../frontend/dist /usr/share/nginx/html
```

---

## Backend Dockerfile (`backend/Dockerfile`)

```
FROM python:3.11-slim

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Frontend Dockerfile (`frontend/Dockerfile`)

```
FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# The build output will be copied into the Nginx container
```

---

## Metabase Docker Compose (`infra/metabase/docker-compose.yml`)

```
version: '3.8'
services:
  metabase:
    image: metabase/metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_FILE: /metabase.db
    volumes:
      - ./metabase.db:/metabase.db
```

---

# DevOps & Operations

## DevOps: Docker Compose & Nginx

### Project Services

- **backend**: Django/DRF app, running inside a venv, served by Gunicorn.
- **nginx** (optional): Reverse proxy for backend API and static files.
- **metabase**: Analytics dashboard, connects to the backend's SQLite DB.

---

## Running the Project with Docker Compose

1. **Build and start all services:**
    ```
    make docker-build
    make docker-up
    ```

2. **Stop all services:**
    ```
    make docker-down
    ```

3. **View logs:**
    ```
    make docker-logs
    ```

4. **Open a shell in any service container:**
    ```
    make docker-shell-backend
    make docker-shell-metabase
    make docker-shell-nginx    # (if using Nginx)
    ```

---

## Makefile DevOps Commands

- `make docker-build` – Build all Docker images
- `make docker-up` – Start all services with Docker Compose
- `make docker-down` – Stop all services
- `make docker-logs` – View logs from all services
- `make docker-shell-backend` – Open a shell in the backend container
- `make docker-shell-metabase` – Open a shell in the metabase container
- `make docker-shell-nginx` – Open a shell in the nginx container

---

## API & Admin Access (Dockerized)

- **API Root:** [http://localhost:8000/api/](http://localhost:8000/api/) (or [http://localhost/api/](http://localhost/api/) if using Nginx)
- **API Docs:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Swagger UI:** [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
- **Health Check:** [http://localhost:8000/health/](http://localhost:8000/health/)
- **Django Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Metabase:** [http://localhost:3000/](http://localhost:3000/)

---

## Environment Management

- Copy `backend/.env.example` to `backend/.env` and fill in your secrets and settings.
- All configuration is handled via environment variables for 12factor compliance.

---

## Production & CI/CD

- All linting, formatting, and test coverage checks are run in CI.
- Test coverage must remain above 80% (builds fail otherwise).
- Docker images are built and deployed using the same Dockerfiles and Compose setup.
- For deployment (e.g., on Render.com), use the same Docker and environment configuration.

---

## Best Practices

- All Python/Django commands (including in Docker) run inside a virtual environment.
- The Makefile and Docker Compose provide a consistent interface for local and production workflows.
- All secrets and configuration are managed via environment variables.
- Metabase is included for easy analytics and reporting on your data.

---
