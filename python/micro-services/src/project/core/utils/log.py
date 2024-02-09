# Standard Library
import logging
import sys
from datetime import datetime

# Third Party Library
from pythonjsonlogger import jsonlogger

log_level_mapper = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom class to add required fields in json format
    """

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def setup_logger_format(logger):
    """
    Setting up the logger details which are required
    """
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        "%(timestamp)s %(name)s %(level)s %(message)s %(pathname)s " "%(funcName)s %(lineno)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def convert_log_level_to_number(log_level):
    """
    Converting log level to value
    """
    return log_level_mapper[log_level]
