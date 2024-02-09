# Standard Library
import logging
import os
import sys

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):  # noqa: N805
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager:
    env_prefix = ""

    def __init__(self, config_file=None):
        self.file_type = None
        self.config_file = config_file
        self.configuration = {}
        self.local_configuration = {}
        if config_file:
            if self.validate_file_type():
                getattr(self, f"read_{self.file_type}")()
            else:
                raise ConfigManagerException("File format not supported, allowed configurations on JSON/YAML")

    def get_env_var(self, env_var):
        return os.getenv(f"{self.env_prefix}_{env_var}")

    def validate_file_type(self):
        extension = self.config_file.rsplit(".")[-1].lower()
        if extension in ["json", "yaml"]:
            self.file_type = extension
            return True
        else:
            return False

    @staticmethod
    def wait_forever():
        logger.error("Missing Environment Variables")
        sys.exit(1)

    def get(self, section, key):
        value = self.configuration.get(f"{section}_{key}")
        if value:
            return value
        else:
            raise ConfigManagerException(
                f"Attribute Missing in"
                f" ConfigManager: {key} under the section: {section} {self.configuration} {self.local_configuration}"
            )

    def load_config(self):
        for config in self.config_param:
            key = config.get("key", None)
            section = config.get("section", None)
            if not (key and section):
                continue
            section_key = f"{section}_{key}"
            # Read Environment Variable
            env = config.get("env", "")
            try:
                env_prefix = self.env_prefix if self.env_prefix != "" else None
            except NameError:
                env_prefix = None
            env_detected = False
            if env != "":
                env_name = f"{env_prefix}_{env}" if env_prefix else env
                env_value = os.getenv(env_name, None)
                if env_value:
                    self.configuration[section_key] = env_value
                    continue
                env_detected = True
                # else:
                #    print(F"{env_name} is Mandatory")
                #    self.wait_forever()
            # Read from Local File if available
            if section_key in self.local_configuration:
                self.configuration[section_key] = self.local_configuration[section_key]
                continue
            # Read from Fall Back
            self.configuration[section_key] = config.get("fallback", None)
            if self.configuration[section_key] is None and env_detected:
                print(f"{env_name} is Mandatory")
                self.wait_forever()

    def read_json(self):  # noqa: C901
        from json import loads, decoder

        try:
            with open(self.config_file) as file:
                config_list = loads(file.read())
            self.local_configuration = {}
            for section in config_list:
                if isinstance(config_list[section], dict):
                    for key, value in config_list[section].items():
                        section_key = f"{section}_{key}"
                        if isinstance(value, dict):
                            raise AttributeError("Value cannot contain a list/dict")
                        elif isinstance(value, list):
                            for inner_val in value:
                                if isinstance(
                                    inner_val,
                                    (
                                        dict,
                                        list,
                                    ),
                                ):
                                    raise AttributeError("Value cannot contain a list/dict")
                            self.local_configuration[section_key] = value = " ".join(list(map(str, value)))

                        else:
                            self.local_configuration[section_key] = value
                else:
                    raise AttributeError("Section must be dict")
        except FileNotFoundError:
            print(f"Configuration File at {self.config_file} Missing")
            self.wait_forever()
        except (decoder.JSONDecodeError, AttributeError) as e:
            print(f"Configuration File at {self.config_file} Failed : {e}")
            self.wait_forever()

    def read_yaml(self):
        from yaml import load, FullLoader, parser

        try:
            with open(self.config_file) as file:
                config_list = load(file, Loader=FullLoader)
                for section in config_list:
                    for config_local in config_list[section]:
                        section_key = "{}_{}".format(section, tuple(config_local.keys())[-1])
                        self.local_configuration[section_key] = tuple(config_local.values())[-1]
        except parser.ParserError:
            print(f"Configuration File at {self.config_file} Failed")
            self.wait_forever()
        except FileNotFoundError:
            print(f"Configuration File at {self.config_file} Missing")
            self.wait_forever()
        except AttributeError:
            print(f"Configuration File at {self.config_file} Failed, allows only <Key:Value> pairs")
            self.wait_forever()

    def refresh(self):
        if self.config_file:
            self.__init__(config_file=self.config_file)
        else:
            self.__init__()
        self.load_config()


class ConfigManagerException(Exception):
    pass
