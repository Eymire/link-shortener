#!/bin/sh
set -e

echo "Start migrations..."
alembic upgrade head
echo "Migrations complete!"

exec "$@"
