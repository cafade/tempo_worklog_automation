# Source reference: https://github.com/orgs/python-poetry/discussions/1879

FROM python:3.11-bookworm as builder

RUN pip install poetry==1.7.1

ENV PYTHONUNBUFFERED 1 \
  PYTHONDONTWRITEBYTECODE 1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN  python -m venv '.venv' && \
  poetry install --without dev && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-bookworm as app

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY ./ /app

ENTRYPOINT ["python", "/app/main.py"]
