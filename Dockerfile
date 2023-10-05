FROM python:3.10

WORKDIR /app

RUN apt-get update

RUN apt-get -y install gcc

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

VOLUME [ "/app" ]

EXPOSE 8000

EXPOSE 6379
CMD ["gunicorn", "main:create_app()", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.worker.GunicornWebWorker", "--max-requests", "2", "--reload"]