"""
Environment specific configuration
"""

PYPY_SERVER = {
    "test": "https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple/", # noqa
    "prod": "https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/simple/" # noqa
}


def get_pypi_url(environment):
    """
    Returns the pypi url for a given environment
    """
    try:
        return PYPY_SERVER[environment]
    except KeyError:
        raise KeyError(
            f"No pypi server defined for the '{environment}' environment")
