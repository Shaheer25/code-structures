# Standard Library
from enum import Enum


class MongoVerbs(str, Enum):
    FIND = "find"
    FIND_ONE = "find_one"
    INSERT_ONE = "insert_one"
    INSERT_MANY = "insert_many"
    UPDATE_ONE = "update_one"
    UPDATE_MANY = "update_many"
    AGGREGATE = "aggregate"


class EmailProviders(str, Enum):
    mailGun = "mailGun"
