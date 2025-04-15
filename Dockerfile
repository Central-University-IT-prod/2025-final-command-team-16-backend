FROM python:3.12-slim AS builder
LABEL maintainer="Koalal143" name="Rumiantsev Vladimir"

ARG MODE=prod

ENV MODE=$MODE \
    PYTHONPATH="/app"\
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    \
    SERVER__URL="http://some-url.ru " \
    SERVER__HOST=0.0.0.0 \
    SERVER__PORT=8080 \
    SERVER__COOKIE_MAX_AGE_MINUTES=3600 \
    SERVER__RESET_PASSWORD_TOKEN=secret \
    SERVER__VERIFICATION_TOKEN=secret \
    \
    MAIL__USERNAME=some_username \
    MAIL__PASSWORD=secret \
    MAIL__FROM_EMAIL=some_email@mail.com \
    MAIL__FROM_NAME=some_name \
    MAIL__PORT=1017 \
    MAIL__SERVER=smtp.mail.ru \
    POSTGRES__USERNAME=postgres \
    POSTGRES__PASSWORD=password \
    POSTGRES__HOST=postgres \
    POSTGRES__DATABASE=postgres \
    POSTGRES__PORT=5432 \
    POSTGRES__ECHO=0 \
    \
    REDIS__HOST=redis \
    REDIS__PORT=6379 \
    REDIS__DATABASE=0

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --only main

FROM builder AS final

COPY --from=builder /app /app
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY . /app

WORKDIR /app/

CMD ["sh", "-c", "poetry run alembic upgrade head \
     && poetry run uvicorn --host $SERVER__HOST --port $SERVER__PORT src.main:app"]
