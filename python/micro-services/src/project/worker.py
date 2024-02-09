# Third Party Library
from celery_app import celery_app

# Register the service so celery worker can register and distribute the task across project orchestrators
INSTALLED_SERVICES = [
]
celery_app.autodiscover_tasks(INSTALLED_SERVICES, force=True)
