# Standard Library
import logging

# Project Library
from project.core.utils.exceptions import ProjectException, DataNotFoundException, DbException
from project.core.utils.log import setup_logger_format
from project.core.utils.mongodb import db

logger = logging.getLogger(__name__)
setup_logger_format(logger)


class GenericUtils:
    def __init__(self):
        pass

    @staticmethod
    def connect_db(collection):
        """
        This method is useful to get the collection instance.
        """
        try:
            db_connection = db[collection]
            return db_connection
        except Exception as err:
            logger.error(f"Failed to connect db {str(err)}")
            raise ProjectException(str(err))

    @staticmethod
    async def find_one_record(collection, query, projection=None, find_exists=False):
        """
        This method is useful to call the find_one method
        on collections.
        """
        db_instance = GenericUtils.connect_db(collection)
        if projection:
            query = [query, projection]
        else:
            query = [query]

        try:
            result = await db_instance.find_one(*query)
            if result:
                return result
            else:
                if find_exists:
                    return False
                else:
                    raise DataNotFoundException(
                        f"Data not found in {collection} collection with provided query {query}"
                    )

        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {str(err)}")

    @staticmethod
    async def insert_one(collection, query):
        """
        This method is useful to call the insert_one method
        on collections.
        """
        db_instance = GenericUtils.connect_db(collection)
        try:
            result = await db_instance.insert_one(query)
            return result
        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {str(err)}")

    @staticmethod
    async def insert_many(collection, documents):
        """
        This method is useful to call the insert_many method
        on collections.
        """
        db_instance = await GenericUtils.connect_db(collection)
        try:
            result = db_instance.insert_many(documents)
            return result
        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {str(err)}")
        
    @staticmethod
    def update_one(collection, find_record, update_data):
        """
        This method is useful to call the update_one method
        on collections.
        """
        db_instance = GenericUtils.connect_db(collection)
        try:
            result = db_instance.update_one(find_record, update_data)
            return result
        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {str(err)}")

    @staticmethod
    async def find_to_list(collection, search_query, projection=None, query_filters=None, find_exists=False):
        """
        This method is useful to call the find method
        on collections.
        """
        db_instance = GenericUtils.connect_db(collection)
        if projection:
            query = [search_query, projection]
        else:
            query = [search_query]
        try:
            if query_filters:
                result = (
                    await db_instance.find(*query)
                    .sort(query_filters["sort_by"], query_filters["sort_mode"])
                    .limit(query_filters["per_page"])
                    .skip((query_filters["page"] - 1) * query_filters["per_page"])
                    .to_list(None)
                )
            else:
                result = await db_instance.find(*query).to_list(None)
            if not result:
                if find_exists:
                    return result
                else:
                    raise DataNotFoundException(
                        f"Data not found in {collection} collection with provided query {query}"
                    )
            return result
        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {err}")

    @staticmethod
    async def find_aggregate(collection, search_query):
        """
        This method is useful to call the aggregate
        on collections.
        """
        db_instance = GenericUtils.connect_db(collection)
        try:
            response = db_instance.aggregate(search_query)
            result = [document for document in await response.to_list(None)]
            if not result:
                raise DataNotFoundException(f"Data not found in {collection} collection with provided query")
            return result
        except DbException as err:
            logger.error(str(err))
            raise DbException(f"Database operation failed due to error {str(err)}")


generic_utils = GenericUtils()
