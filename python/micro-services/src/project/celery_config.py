# Third Party Library
from celery.schedules import crontab

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "mongodb",
    "port": 27017,
    "database": "jobs",
    "taskmeta_collection": "stock_taskmeta_collections",
}
CELERY_TRACK_STARTED = True
# used to schedule services periodically and passing optional arguments
# Can be very useful. Celery does not seem to support scheduled task but only periodic
CELERYBEAT_SCHEDULE = {
    "every-minute": {
        "task": "services.add",
        "schedule": crontab(minute="*/1"),
        "args": (1, 2),
    }
}
