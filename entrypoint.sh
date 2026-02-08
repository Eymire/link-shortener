#!/usr/bin/env bash

echo "Start migrations..."
uv run alembic upgrade head
echo "Migrations complete!"

exec "$@"
