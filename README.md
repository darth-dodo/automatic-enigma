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
