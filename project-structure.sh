#!/bin/bash

set -e

echo "Creating backend, frontend, infra, docs, and CI/CD structure..."

# Backend
mkdir -p backend/{apps,config,staticfiles}
mkdir -p backend/apps/{clinic,users}
mkdir -p backend/apps/clinic/{api,management/commands,migrations}
mkdir -p backend/apps/users/{api,migrations}
touch backend/{manage.py,requirements.txt,.env.example,Dockerfile,pytest.ini,.pre-commit-config.yaml,locustfile.py}
touch backend/config/{__init__.py,asgi.py,wsgi.py,settings.py,urls.py}
touch backend/apps/clinic/{admin.py,models.py,tests.py}
touch backend/apps/clinic/api/{serializers.py,urls.py,views.py}
touch backend/apps/clinic/management/commands/{populate_db.py,purge_db.py}
touch backend/apps/users/{admin.py,models.py,tests.py}
touch backend/apps/users/api/{serializers.py,urls.py,views.py}

# Frontend
mkdir -p frontend/src
touch frontend/{package.json,tsconfig.json,tailwind.config.js,Dockerfile}

# Infra (DevOps)
mkdir -p infra/nginx
mkdir -p infra/metabase
touch infra/nginx/{nginx.conf,Dockerfile}
touch infra/metabase/docker-compose.yml
touch docker-compose.yml

# GitHub Actions CI/CD
mkdir -p .github/workflows
touch .github/workflows/ci.yml

# Docs and tests
mkdir -p docs
touch README.md
touch Makefile
touch docs/{API.md,codebase.md,learning_resources.md}
mkdir -p tests/e2e
touch tests/e2e/{playwright.config.ts,clinic.spec.ts}

echo "Project structure created successfully!"
