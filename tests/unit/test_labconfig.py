import os
from tempfile import TemporaryDirectory
from src.labs.labconfig import ConfigError, gencfg, loadcfg


def test_configerror_message():
    """
    ConfigError instances should have an error message
    """
    # Given
    error = ConfigError("error msg")

    # When
    msg = error.message

    # Then
    assert "error msg" == msg


def test_gencfg_uses_default_log_path():
    """
    gencfg uses /tmp/log/labs/ as default log path
    """
    # Given a tmp config file
    with TemporaryDirectory() as tempdir:
        filepath = os.path.join(tempdir, "config.yaml")

        # When the config is written in the config file
        gencfg(filepath, "SKU123")

        # Then the config uses /tmp/log/labs/ as default logging path
        config = loadcfg(filepath)
        assert config["rhtlab"]["logging"]["path"] == "/tmp/log/labs/"
