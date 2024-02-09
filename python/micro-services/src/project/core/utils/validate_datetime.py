# Standard Library
import logging
import re

# Project Library
from project.core.utils.log import setup_logger_format

logger = logging.getLogger(__name__)
setup_logger_format(logger)


def validate_iso_format_and_convert(date_string):
    """
    This method validate the expiry date
    """
    try:
        regex = (
            r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):"
            r"([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|z)?$"
        )
        match_iso8601 = re.compile(regex).match
        if match_iso8601(date_string) is not None:
            if "Z" in date_string:
                return True, date_string.replace("Z", "+00:00")
            elif "z" in date_string:
                return True, date_string.replace("z", "+00:00")
            else:
                return (
                    False,
                    "Allowed date should be in UTC and ISO format "
                    "2022-06-20T01:45:36.123Z or 2022-06-20T01:45:36.123z",
                )
    except Exception as err:
        logger.error(err)
        return (
            False,
            f"Date format is not correct failed with error {err}, date should be in UTC and ISO format"
            f"2022-06-20T01:45:36.123Z or 2022-06-20T01:45:36.123z",
        )
    return (
        False,
        "Invalid date format, date should be in UTC and ISO format "
        "2022-06-20T01:45:36.123Z or 2022-06-20T01:45:36.123z",
    )
