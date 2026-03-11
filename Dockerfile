FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /src/
WORKDIR /src

ENV DJANGO_DEBUG_FALSE=1
ENV DJANGO_SECRET_KEY=secret
ENV DJANGO_ALLOWED_HOST=localhost

RUN uv sync --frozen --no-dev

COPY src /src

RUN uv run python manage.py collectstatic --no-input

CMD ["uv", "run", "gunicorn", "--bind", ":8888", "superlists.wsgi:application"]