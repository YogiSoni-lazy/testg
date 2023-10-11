"""
Package-level Configuration.
This is different from the config controlled labs.labconfig,
which manages lab-level config
"""

import configparser
from pathlib import Path


def load():
    cfg = configparser.ConfigParser()
    cfg.read(Path(__file__).with_name("config.ini"))
    return cfg
