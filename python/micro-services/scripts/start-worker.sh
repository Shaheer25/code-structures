#! /usr/bin/env sh

# Start celery
exec celery worker --workdir /usr/local/lib/python3.8/site-packages/project --app=worker.celery_app --pool=prefork  --loglevel=INFO --beat  --concurrency=10 --autoscale=8,1
