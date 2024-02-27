FROM python:3.12-slim as python-base

ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools wheel \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as poetry-base

COPY --from=python-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY ../poetry.lock pyproject.toml ./

RUN poetry lock
RUN poetry check

FROM poetry-base as app

COPY .. .

RUN poetry install --no-interaction --no-ansi --only main

WORKDIR /app

CMD ["poetry", "run", "python", "-m", "app"]
