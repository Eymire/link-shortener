FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . .

CMD [ "uv", "run", "uvicorn", "--factory", "src.main:create_app", "--host", "0.0.0.0", "--workers", "4", "--no-server-header", "--no-date-header", "--no-use-colors" ]
