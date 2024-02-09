from project.configs.config_manager import ConfigManager, ConfigManagerException, Singleton

ConfigManagerException = ConfigManagerException

# Project Library
from project.configs.config_manager import ConfigManager, ConfigManagerException, Singleton

ConfigManagerException = ConfigManagerException


class AppConfig(ConfigManager, metaclass=Singleton):
    env_prefix = "PROJECT"

    config_param = [
    ]

    def __init__(self):
        print("Initialized Config Manager")
        try:
            config_file = self.get_env_var("CONFIG")
            if config_file is None:
                raise KeyError
        except KeyError:
            config_file = "/app/config/project.yaml"
        print(f"ENV Considered from path: {config_file}")
        super().__init__(config_file=config_file)


config = AppConfig()
config.load_config()
