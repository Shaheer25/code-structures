FROM python:3.8 as BASE

COPY . .
RUN pip install -r requirements.txt && python setup.py sdist

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

LABEL version="0.1.0"

RUN pip install -U "celery[redis]"

# Setup FS
WORKDIR /
RUN mkdir -p /app/config
RUN mkdir -p /app/tests
RUN mkdir -p /app/dist

# copying third-party wheels
COPY requirements.txt /app/requirements.txt
COPY configurations/project.yaml /app/config/project.yaml
COPY --from=BASE dist/ /app/dist/
COPY scripts/prestart.sh /app

RUN mkdir -p /var/log/project/ && \
    pip install -r /app/requirements.txt && \
    pip install /app/dist/project* && \
    rm -r /app/dist/*
