#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running migrations..."
  alembic upgrade head
fi

exec python run.py