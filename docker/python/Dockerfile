FROM python:3.11.7-slim-bookworm as python-base

WORKDIR "/app"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

# 初回起動用image
FROM python-base as init

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python -

# 開発環境用image
FROM init as dev
COPY ./app/pyproject.toml ./app/poetry.lock  ./

RUN poetry install --no-root

# 本番環境build用image
FROM init as builder
COPY ./app/pyproject.toml ./app/poetry.lock  ./

RUN poetry install --no-dev

# 本番環境用image
FROM python-base as prod
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY /app/src /app/src
COPY /app/start_app.sh /app/start_app.sh

# サーバー起動
ENTRYPOINT ["bash", "start_app.sh"]
