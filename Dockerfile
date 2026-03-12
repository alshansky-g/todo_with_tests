FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /src/
WORKDIR /src

ENV VIRTUAL_ENV=/src/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv sync --frozen --no-dev --no-cache

COPY src /src

RUN python manage.py collectstatic --no-input
RUN adduser --uid 1234 user

USER user

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]
