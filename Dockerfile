FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --only main

COPY src README.md ./
RUN poetry install --only-root --no-interaction

EXPOSE 5000

CMD ["poetry", "run", "python", "-m", "app"]