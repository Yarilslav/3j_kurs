#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-false}" = "true" ] && [ "${1:-}" = "python" ] && [ "${2:-}" = "run.py" ]; then
  echo "Running migrations..."
  alembic upgrade head
fi

exec "$@"
