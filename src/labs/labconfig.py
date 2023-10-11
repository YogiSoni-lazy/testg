# Lab Configuration Tool (in Python3)
#
# Chris Tusa <ctusa@redhat.com>
# (C)opyright 2020 : Red Hat, Inc. - see LICENSE
#

import yaml
import os
import tempfile


class ConfigError(BaseException):
    def __init__(self, message, object=None):
        self.message = message


def get_course_sku():
    """
    Return the SKU number of the course
    :return: unique course SKU
    """
    config = loadcfg()
    sku = config['rhtlab']['course']['sku']
    if sku is None:
        raise ConfigError("SKU is not configured")
    return sku


def _get_config_path(filename):
    # If no filename argument is passed,
    # then try to load the path from the RHT_LABS_CONFIG_PATH env variable.
    # RHT_LABS_CONFIG_PATH is useful for testing.
    # If none is set, then use the default
    default_filename = "~/.grading/config.yaml"
    filename = filename or os.environ.get(
        "RHT_LABS_CONFIG_PATH",
        default_filename
    )

    return os.path.expanduser(filename)


def loadcfg(filename=None):
    """
    Load configuration data from a YAML file
    """

    filename = _get_config_path(filename)
    if os.path.exists(filename):
        # Open the config file and parse Yaml
        try:
            with open(filename) as f:
                cfgdata = yaml.load(f, Loader=yaml.FullLoader)
                if cfgdata and list(cfgdata)[0] == 'rhtlab':
                    return cfgdata
                else:
                    raise ConfigError(
                        "Invalid configuration file %s, invalid format"
                        % filename)
        except yaml.YAMLError as err:
            raise ConfigError("Invalid configuration file %s" % filename, err)
    else:
        raise ConfigError("Configuration file %s not found" % filename)


def savecfg(cfgdata, filename=None):
    """
    Saves the configuration to a yaml file.
    'cfgdata' should be passed in as a Python dictionary
    'filename' should be pre-validated through the passing function
    """
    filename = _get_config_path(filename)
    dir = os.path.split(filename)[0]
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(filename, "w") as cfgfile:
        yaml.dump(cfgdata, cfgfile)
        cfgfile.close()


def setsku(sku, filename=None):

    try:
        cfgdata = loadcfg(filename)
        cfgdata['rhtlab']['course']['sku'] = sku.lower()
        savecfg(cfgdata, filename)
    except ConfigError:
        gencfg(sku=sku)


def gencfg(filename=None, sku=None, force=False):
    """
    Create a default configuration file
    """

    filename = _get_config_path(filename)

    if os.path.exists(filename) and not force:
        raise ConfigError("Configuration file exists %s" % filename)

    cfgdata = {'rhtlab':
               {
                 'course':
                 {
                   'sku': sku.lower()
                 },
                 'logging':
                 {
                   'path': get_default_log_path(),
                   'level': 'error'
                 }
                }
               }

    savecfg(cfgdata, filename)

    return cfgdata


def get_default_log_path():
    return os.path.join(
        tempfile.gettempdir(),
        "log",
        "labs",
        ""
    )


def get_version_lock(filename='/etc/rht'):
    if os.path.exists(filename):
        with open(filename, 'r') as reader:
            line = reader.readline()
            while line != '':
                var = line.split('"')
                if var[0] == "RHT_VERSION_LOCK=":
                    print("Version lock is %s" % var[1])
                    return var[1]
                line = reader.readline()
    return None


def is_dev_mode():
    return os.environ.get("DEV", None) is not None
