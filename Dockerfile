FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /src/
WORKDIR /src

RUN uv sync --frozen --no-dev

COPY src /src

CMD ["uv", "run", "gunicorn", "--bind", ":8888", "superlists.wsgi:application"]