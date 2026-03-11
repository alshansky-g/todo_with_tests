FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv pip install --system "django<6" "gunicorn" "whitenoise"

COPY src /src

WORKDIR /src

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]
