FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Встановлюємо Poetry в контейнер.
RUN pip install --no-cache-dir poetry
# через pip, щоб Dockerfile був простим і відтворюваним.

# Робочий каталог:
WORKDIR /app

# для кращого кешування копіюється:
COPY pyproject.toml poetry.lock* /app/


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


COPY app /app/app
COPY run.py /app/run.py

# Порт:
EXPOSE 8000

CMD ["python", "run.py"]
