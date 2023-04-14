FROM python:3.10.8-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN set -ex \
    & poetry install --no-dev

COPY . .

CMD ["poetry", "run", "python", "run_bot.py"]
