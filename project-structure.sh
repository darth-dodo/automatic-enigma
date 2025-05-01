#!/bin/bash

# Project root
mkdir -p automatic-enigma/{backend/{apps,config,tests,management/commands},frontend/src,infra/nginx,infra/metabase,.github/workflows,docs,tests/e2e}
touch automatic-enigma/{README.md,Makefile}
touch automatic-enigma/backend/{requirements.txt,.env.example,Dockerfile,manage.py}
touch automatic-enigma/backend/config/{settings.py,urls.py,wsgi.py,asgi.py}
touch automatic-enigma/frontend/{package.json,tsconfig.json,tailwind.config.js,Dockerfile}
touch automatic-enigma/infra/nginx/{nginx.conf,Dockerfile}
touch automatic-enigma/infra/metabase/docker-compose.yml
touch automatic-enigma/.github/workflows/ci.yml
touch automatic-enigma/docs/{API.md,codebase.md,learning_resources.md}
touch automatic-enigma/tests/e2e/{playwright.config.ts,clinic.spec.ts}
