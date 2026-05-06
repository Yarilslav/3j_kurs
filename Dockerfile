FROM python:3.11-slim

ARG INSTALL_DEV=false

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_RELOAD=false

# Встановлюємо Poetry в контейнер.
RUN pip install --no-cache-dir poetry
# через pip, щоб Dockerfile був простим і відтворюваним.

# Робочий каталог:
WORKDIR /app

# для кращого кешування копіюється:
COPY pyproject.toml poetry.lock* /app/


RUN poetry config virtualenvs.create false \
    && if [ "$INSTALL_DEV" = "true" ]; then \
        poetry install --with dev --no-interaction --no-ansi --no-root; \
    else \
        poetry install --only main --no-interaction --no-ansi --no-root; \
    fi


COPY app /app/app
COPY alembic /app/alembic
COPY assets /app/assets
COPY alembic.ini /app/alembic.ini
COPY run.py /app/run.py
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh \
    && adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

# Порт:
EXPOSE 8000

USER appuser

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "run.py"]
