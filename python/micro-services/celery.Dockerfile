FROM python:3.8 as BASE

COPY . .
RUN pip install -r requirements.txt && python setup.py sdist

FROM python:3.8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN mkdir app && chown -R root:root /app
WORKDIR /app

# auto reload app if installed as dev version
ARG INSTALL_DEV
RUN if [ ! -z "$INSTALL_DEV" ]; then pip install watchdog[watchmedo]; fi
ENV STARTUP=${INSTALL_DEV:+./start-worker-reload.sh}
ENV STARTUP=${STARTUP:-./start-worker.sh}

# install dependencies
COPY requirements.txt .
COPY configurations/project.yaml /app/config/project.yaml
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
COPY --from=BASE dist/ /app/dist/
RUN pip install /app/dist/project*

# copy content
COPY scripts/start-worker.sh .
COPY scripts/start-worker-reload.sh .

#start worker
ENTRYPOINT ["sh","start-worker.sh"]
