"""
    Generic Code Base
"""
# Standard Library
import logging

# Third Party Library
from pymongo.errors import PyMongoError

# Project Library
from project.core.utils.enums import MongoVerbs
from project.core.utils.exceptions import ServiceDBException

logger = logging.getLogger(__name__)


def apply_mongo(collection, verb, *args, **kwargs):  # noqa: C901
    if verb not in list(map(lambda x: x.lower(), MongoVerbs.__dict__.keys())):
        raise ValueError("Mongo Verb is not supported")
    try:
        if verb == MongoVerbs.FIND:
            return [record for record in collection.find(*args, **kwargs)]
        elif verb == MongoVerbs.FIND_ONE:
            result = collection.find_one(*args, **kwargs)
            if result:
                return result
            raise ServiceDBException(f"Failed to find the record with {args} and {kwargs}")
        elif verb == MongoVerbs.INSERT_ONE:
            result = collection.insert_one(*args, **kwargs)
            if result.inserted_id:
                return result.inserted_id
            raise ServiceDBException(f"Failed to insert the record with {args} and {kwargs}")
        elif verb == MongoVerbs.INSERT_MANY:
            result = collection.insert_many(*args, **kwargs)
            if result.inserted_ids:
                return result.inserted_ids
            raise ServiceDBException(f"Failed to insert the record with {args} and {kwargs}")
        elif verb == MongoVerbs.UPDATE_ONE:
            result = collection.update_one(*args, **kwargs)
            if result.matched_count == 1 and result.modified_count == 1:
                return True
            else:
                raise ServiceDBException(f"Failed to Update the Model, No Match Found for {args} and {kwargs}")
        elif verb == MongoVerbs.UPDATE_MANY:
            result = collection.update_many(*args, **kwargs)
            if result.matched_count != 0 and result.modified_count != 0:
                return True
            raise ServiceDBException(f"Failed to Update the Model, No Match Found for {args} and {kwargs}")
    except PyMongoError as e:
        raise ServiceDBException(str(e))
