import os
from configparser import Error
from git import GitConfigParser


def username():
    return _get_value("user", "name")


def email():
    return _get_value("user", "email")


def _get_value(section, option):
    config = GitConfigParser(os.environ.get("GIT_CONFIG"))
    try:
        return config.get_value(section, option)
    except (TypeError, Error):
        return None
