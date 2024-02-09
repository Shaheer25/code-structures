# Standard Library
import logging

# Project Library
from project.core.utils.log import setup_logger_format

logger = logging.getLogger(__name__)

setup_logger_format(logger)


def generate_metadata(base_url, end_url, page, per_page, document_count, page_count):
    """
    This method returns the meta data
    """
    logger.info("Initiating the generate metadata method to get meta data")
    meta_data = {
        "page": page,
        "per_page": per_page,
        "page_count": page_count,
        "total_count": document_count,
        "links": [
            {"self": f"{base_url}{end_url}?page={page}&per_page={per_page}"},
            {"first": f"{base_url}{end_url}?page={1}&per_page={per_page}"},
            {"previous": f"{base_url}{end_url}?page={1 if page == 1 else page - 1}&per_page={per_page}"},
            {"next": f"{base_url}{end_url}?page={page + 1}&per_page={per_page}"},
            {"last": f"{base_url}{end_url}?page={page_count}&per_page={per_page}"},
        ],
    }
    return meta_data
