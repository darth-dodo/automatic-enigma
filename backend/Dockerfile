FROM python:3.11-slim

# Create app directory and set up venv
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files (optional, for production)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use Gunicorn for production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
