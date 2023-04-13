FROM python:3.9.16-slim
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock .

RUN set -ex \
    & poetry install

COPY . .

CMD ["poetry", "run", "python", "serve_with_monitoring.py"]