# Third Party Library
import pytest

# Project Library
from project.config.test_project_config import AppConfig, ConfigManagerException


def test_configuration_case1():
    """
    Verify the happy path
    """
    config = AppConfig()
    config.load_config()
    config.get(section="internals", key="production")
    assert isinstance(config, AppConfig)


def test_configuration_case2():
    """
    Verify if the ConfigManagerException is raised on fetching non existent value
    """
    config = AppConfig()
    config.load_config()
    with pytest.raises(ConfigManagerException):
        config.get(section="internals", key="unknown_value")
