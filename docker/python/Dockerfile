FROM python:3.11.7-slim-bookworm

WORKDIR "/app"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

ENV PYTHONPATH="/app"

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python -

COPY ./app/pyproject.toml ./app/poetry.lock  ./

RUN poetry install --no-root

# uvicorn起動
# ENTRYPOINT ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
