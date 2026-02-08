## Link Shortener

FastAPI service that creates short links, stores them in Postgres, and caches redirects in Redis.

### Features

- Create short links with configurable length and lifetime
- Redirect short codes to original URLs
- Redis cache for fast redirects
- Alembic migrations on container start

### Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy async + asyncpg
- Redis (async)
- Alembic

### API

- `POST /links` -> create a short link
- `DELETE /links/{short_code}` -> remove a short link
- `GET /{short_code}` -> redirect to original URL

The OpenAPI docs are available only when `APP_ENVIRONMENT=development` at `/docs`, `/redoc` and `/openapi.json`.

### Configuration

Create a `.env` file in the project root with these variables:

```
# database
DB_HOST=postgres
DB_NAME=app
DB_USER=app_user
DB_PASSWORD=postgres_password

# redis
REDIS_HOST=redis
REDIS_PASSWORD=redis_password

# compose
COMPOSE_APP_PORT=8000
COMPOSE_APP_WORKERS_COUNT=2
```

### Run With Docker

1. Build and start services:

	```bash
	docker compose up --build
	```

2. The API is available at `http://localhost:${COMPOSE_APP_PORT}`.

Migrations run automatically on container start via [entrypoint.sh](entrypoint.sh).

### Run Locally

1. Install dependencies (requires Python 3.13 and `uv`):

	```bash
	uv sync --locked
	```

2. Apply migrations:

	```bash
	uv run alembic upgrade head
	```

3. Start the server:

	```bash
	uv run uvicorn --factory src.main:create_app --port 8000 --reload
	```

### Notes

- Short codes are stored with an expiration timestamp but are not currently purged automatically.
- Redirects are cached in Redis for `APP_LINK_CACHED_LIFETIME_MINUTES`.
