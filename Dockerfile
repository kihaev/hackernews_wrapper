FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update

RUN apt-get -y install gcc

COPY pyproject.toml /app/

COPY poetry.lock /app/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

VOLUME [ "/app" ]

EXPOSE 8080

CMD ["gunicorn", "main:create_app()", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.worker.GunicornWebWorker", "--max-requests", "2", "--reload"]