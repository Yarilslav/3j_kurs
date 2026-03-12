# Base image with Python runtime
FROM python:3.11-slim

# Keep Python from writing .pyc files and buffer stdout for logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Poetry in the container.
# We install via pip to keep the Dockerfile simple and reproducible.
RUN pip install --no-cache-dir poetry

# Set the working directory for the app.
WORKDIR /app

# Copy dependency metadata first for better layer caching.
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to install packages into the system environment.
# We use --no-root so the project itself is not installed before source is copied.
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the source code after dependencies are installed.
COPY src /app/src

# Expose the port that Uvicorn will listen on.
EXPOSE 8000

# Run the FastAPI app with auto-reload for development.
# --reload watches the source directory for changes.
CMD ["poetry", "run", "uvicorn", "praktychni_3j_kurs.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
