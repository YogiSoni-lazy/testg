from unittest.mock import patch
from labs.labload import loadcache


@patch("labs.labconfig.loadcfg")
def test_logdir(loadcfg):
    """
    loadcache() returns an empty dict when a sku module is not found
    """

    # Given labconfig.loadcfg() returns a config with a missing sku
    loadcfg.return_value = {
        "rhtlab": {"course": {"sku": "some_missing_module"}}
    }

    # When loading the cache
    cache = loadcache()

    # Then the cache is an empty dictionary
    assert cache == {}
