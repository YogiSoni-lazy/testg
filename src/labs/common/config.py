import os
import json
import configparser
from typing import List, Union

import warnings
from pathlib import Path
from abc import ABC, abstractmethod

from labs.common.userinterface import echo


def parse_config(filenames: List[Union[Path, str]]):
    """
    Parse the course configuration from INI files.

    You can define more than one file, for example:
     - a default config file that contains the default config for production.
     - a custom config file that contains custom config for dev environments

    The files do not need to exist.

    You can also define an additional file by using the
    COURSE_CUSTOM_CONFIG_FILE variable (useful for tests)

    Each config file must contain the [course_config] section.

    Args:
        filenames: the absolute path to the config files.
    """
    customfile = os.getenv("COURSE_CUSTOM_CONFIG_FILE")

    if customfile:
        filepaths = filenames + [customfile]
    else:
        filepaths = filenames

    parser = configparser.ConfigParser()
    # Do no lowercase config keys
    parser.optionxform = str

    parser.read(filepaths)

    return CourseConfig(parser)


class CourseConfig:

    def __init__(self, parser: configparser.ConfigParser) -> None:
        self.conf = parser["course_config"]
        # Set all config values as env variables
        # for convencience in other modules
        # but do not override the env variables that have already been set
        config_only_keys = [k for k in self.conf.keys() if k not in os.environ]
        os.environ.update({k: self.conf[k] for k in config_only_keys})

    def get(self, key: str):
        """
        Get a config value from an env variable or from the ConfigParser
        """
        return os.getenv(key, self.conf[key])

    def get_boolean(self, key: str):
        """
        Get a bool value an env variable or from the ConfigParser
        """
        env_value = os.getenv(key, "").lower()
        return env_value in ["yes", "1", "true"] or self.conf.getboolean(key)

    def is_dev(self):
        """
        Configuration has been set for a dev environment
        """
        return self.get_boolean("LOCAL_DEV")

    def is_prod(self):
        """
        Configuration has been set for a prod environment
        """
        return not self.is_dev()


class ClassroomConfigFile(ABC):

    """DEPRECATED: Use `labs.common.config.parse_config` instead

    Abstract classroom config file.
    """

    filepath: str
    workdir: str

    def __init__(self, filepath: str, workdir: str):
        """
        :param filepath: Absolute path of the file where the config is stored
        :param workdir: Absolute path of the lab working dir
        """

        warnings.warn(
            "This class is deprecated. "
            "Use config.parse_config() instead",
            category=DeprecationWarning
        )

        self.filepath = filepath
        self.workdir = workdir

    @abstractmethod
    def load(self) -> "ClassroomConfigFile":
        pass

    @abstractmethod
    def save(self, output: bool = True):
        pass


class ClassroomConfigJsonFile(ClassroomConfigFile):

    """DEPRECATED: Use `labs.common.config.parse_config` instead

    Classroom config as a JSON file
    """

    def load(self):
        """
        Reads the config from a JSON file
        """
        try:
            with open(self.filepath) as configfile:
                items = json.load(configfile)
                self.__dict__.update(items)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

        return self

    def save(self, output: bool = True):
        """
        Saves the dictionary as a JSON file
        """
        with open(self.filepath, 'w') as outfile:
            json.dump(self.__dict__, outfile, indent=2)

        if output:
            echo(f"Saved configuration in {self.filepath}")


def default_config_path(filename: str):
    """
    Returns a default config file path in ~/.grading/, given a filename
    """
    return Path.home().joinpath(".grading").joinpath(filename)
