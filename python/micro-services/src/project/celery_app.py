# Third Party Library
from celery import Celery
from celery.utils.log import get_task_logger

# Project Library
from project.configs.project_config import config

CELERY_BROKER = config.get(section="celery", key="broker")
CELERY_BACKEND = config.get(section="celery", key="backend")


# Create the celery app and get the logger
celery_app = Celery("services", broker=CELERY_BROKER, backend=CELERY_BACKEND)
# celery_app = Celery('services', broker='mongodb://mongodb:27017/jobs')
# celery_app.config_from_object("celery_config")
logger = get_task_logger(__name__)
