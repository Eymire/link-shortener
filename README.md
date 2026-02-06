## Link Shortener API

FastAPI service for creating short links and redirecting to original URLs. Uses PostgreSQL for persistence and Redis for cache.

### Features
- Short-link creation with configurable length and TTL
- Redirect endpoint with Redis caching
- Async PostgreSQL (SQLAlchemy + asyncpg)
- Alembic migrations

### Tech Stack
- Python 3.13
- FastAPI + Uvicorn
- PostgreSQL 17
- Redis 8
- Alembic, SQLAlchemy (async)

### Quick Start (Docker)
1. Create a `.env` file in the project root:

```env
APP_ENVIRONMENT=development
APP_ROOT_PATH=
APP_LINK_LENGTH=8
APP_LINK_LIFETIME_DAYS=30
APP_LINK_CACHED_LIFETIME_MINUTES=60

DB_HOST=postgres
DB_NAME=link_shortener
DB_USER=link_user
DB_PASSWORD=link_password

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=redis_password
REDIS_MAX_CONNECTIONS=10

API_WORKERS_COUNT=2
```

2. Build and run services:

```bash
docker compose up --build
```

3. Run migrations (in another terminal):

```bash
docker compose exec app uv run alembic upgrade head
```

The API is available at `http://localhost:8000`.
Docs are enabled only when `APP_ENVIRONMENT=development`.

### Local Development (uv)
1. Install dependencies:

```bash
uv sync
```

2. Create `.env` (see template above). Use your local DB/Redis hosts.

3. Run migrations:

```bash
uv run alembic upgrade head
```

4. Start the API:

```bash
uv run uvicorn --factory src.main:create_app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints
- `POST /links`
	- Body: `{ "url": "https://example.com" }`
	- Response: `{ "url": "https://example.com", "short_code": "Ab12Cd34", "expires_at": "2026-02-06T12:00:00Z" }`
- `DELETE /links/{short_code}`
- `GET /{short_code}`
	- Redirects to the original URL

### Configuration
All settings are loaded from `.env` and are prefixed per section.

#### App
- `APP_ENVIRONMENT`: `development` or `production`
- `APP_ROOT_PATH`: optional root path (useful behind a proxy)
- `APP_LINK_LENGTH`: length of the generated short code
- `APP_LINK_LIFETIME_DAYS`: link expiration window
- `APP_LINK_CACHED_LIFETIME_MINUTES`: Redis cache TTL

#### Database
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

#### Redis
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`
- `REDIS_PASSWORD`
- `REDIS_MAX_CONNECTIONS`

### Notes
- The redirect endpoint caches resolved URLs in Redis for faster lookups.
- Links are stored with an expiration timestamp; cleanup is not automated yet.
