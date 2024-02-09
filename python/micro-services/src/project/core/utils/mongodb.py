# Third Party Library
import motor.motor_asyncio
from pymongo import MongoClient

# Project Library
from project.configs.project_config import config
from project.configs.settings import UUID_REPRESENTATION

MONGO_URL = config.get(section="mongodb", key="url")
MONGO_DATABASE = config.get(section="mongodb", key="database")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, uuidRepresentation=UUID_REPRESENTATION)
client_sync = MongoClient(MONGO_URL)  # TO BE USED INSIDE CELERY AS CELERY DOES NOT SUPPORT ASYNCIO

db = client[MONGO_DATABASE]
db_sync = client_sync[MONGO_DATABASE]  # TO BE USED INSIDE CELERY AS CELERY DOES NOT SUPPORT ASYNCIO
# if db[PUSH_NOTIFICATION_AUTHORIZATION].index_information():
#     print(db[PUSH_NOTIFICATION_AUTHORIZATION].index_information())
# else:
#     db[PUSH_NOTIFICATION_AUTHORIZATION].create_index("generatedTime", expireAfterSeconds=86400)
