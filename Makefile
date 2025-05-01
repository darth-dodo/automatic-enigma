PYTHON_VENV=.venv
PYTHON=$(PYTHON_VENV)/bin/python
PIP=$(PYTHON_VENV)/bin/pip

# Create venv and install requirements (idempotent)
venv:
	test -d $(PYTHON_VENV) || python3 -m venv $(PYTHON_VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run Django commands inside venv
migrate: venv
	$(PYTHON) manage.py migrate

makemigrations: venv
	$(PYTHON) manage.py makemigrations

shell: venv
	$(PYTHON) manage.py shell

run: venv
	$(PYTHON) manage.py runserver 0.0.0.0:8000

createsuperuser: venv
	$(PYTHON) manage.py createsuperuser

populate: venv
	$(PYTHON) manage.py populate_db

purge: venv
	$(PYTHON) manage.py purge_db

collectstatic: venv
	$(PYTHON) manage.py collectstatic --noinput

lint: venv
	$(PYTHON_VENV)/bin/black backend/
	$(PYTHON_VENV)/bin/flake8 backend/
	$(PYTHON_VENV)/bin/isort backend/

format: venv
	$(PYTHON_VENV)/bin/black backend/
	$(PYTHON_VENV)/bin/isort backend/

test: venv
	$(PYTHON_VENV)/bin/pytest --disable-warnings

cov: venv
	$(PYTHON_VENV)/bin/pytest --cov=backend/apps --cov-report=term-missing

install-precommit: venv
	$(PYTHON_VENV)/bin/pip install pre-commit
	$(PYTHON_VENV)/bin/pre-commit install

clean:
	rm -rf $(PYTHON_VENV) .pytest_cache .mypy_cache

# Docker targets
docker-build:
	docker build -t automatic-enigma-backend ./backend

docker-run:
	docker run --rm -it -p 8000:8000 automatic-enigma-backend

docker-shell:
	docker run --rm -it automatic-enigma-backend /bin/bash

.PHONY: venv migrate makemigrations shell run createsuperuser populate purge collectstatic lint format test cov install-precommit clean docker-build docker-run docker-shell
