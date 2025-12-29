#!/bin/sh
set -e

echo "⏳ Waiting for database to be ready..."

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "✅ Database is up"

echo "🚀 Running Alembic migrations..."
cd /app/api && alembic upgrade head

echo "🎯 Starting FastAPI application..."
exec "$@"
