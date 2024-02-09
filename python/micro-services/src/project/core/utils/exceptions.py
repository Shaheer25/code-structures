"""Project Exceptions"""
# Standard Library
import logging

logger = logging.getLogger(__name__)


class ProjectException(Exception):
    """Exception raised by every module in the Project package."""

    def __init__(self, msg=None):
        """

        Args:
            msg (str): human friendly error message.
        """

        if msg is None:
            msg = "Project Exception"
        logger.exception(msg)
        super().__init__(msg)


class DbException(ProjectException):
    """Exception raised by every function in the ServiceDB sub-module"""

    pass


class ServiceDBException(ProjectException):
    """Exception raised by every function in the ServiceDB sub-module"""

    pass


class DataNotFoundException(ProjectException):
    pass


class ConnectionException(ProjectException):
    pass


class DriverNotSupported(ProjectException):
    pass


class ImageProcessingError(ProjectException):
    """Custom exceptions class for image processing errors"""

    pass


class TextProcessingError(ProjectException):
    """Custom exceptions class for Text processing errors"""

    pass


class LineProcessingError(ProjectException):
    """Custom exceptions class for Line Drawing errors"""

    pass


class ImageDownloadError(ProjectException):
    pass
