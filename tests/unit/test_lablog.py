# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.

"""Test the :mod:`labs.lablog` module."""

import pytest
import shutil
import tempfile
import pathlib
import logging
import datetime
import sys

import labs.lablog


@pytest.fixture
def setup_test():
    temp_dir = tempfile.mkdtemp()
    config = {"rhtlab": {
        "logging": {"path": temp_dir},
        }
    }
    lab_name = "lab_01_1"
    yield (config, lab_name)
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_logdir(setup_test):
    """Test when path is ending with a ``/`` (``/var/tmp/labs/``)."""
    (config, lab_name) = setup_test
    remove_root_logger_handlers()

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")

    assert expected_file.is_file()
    with open(expected_file) as f:
        assert "==MSG==" in f.read()


def test_lognamesubst(setup_test):
    """Test when path contains ``{lab_name}`` (``/var/tmp/{lab_name}.out``)."""
    (config, lab_name) = setup_test

    expected_file = pathlib.Path(config["rhtlab"]["logging"]["path"])\
        / (lab_name + ".out")
    config["rhtlab"]["logging"]["path"] += "/{lab_name}.out"
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")

    assert expected_file.is_file()
    with open(expected_file) as f:
        assert "==MSG==" in f.read()


def test_logdatetime(setup_test):
    """Test when path contains a date (``/var/tmp/{lab_name}.%Y%m%d``)."""
    (config, lab_name) = setup_test

    today_date = datetime.datetime.now().strftime("%Y%m%d")
    expected_file = pathlib.Path(config["rhtlab"]["logging"]["path"])\
        / ("out." + today_date)
    config["rhtlab"]["logging"]["path"] += "/out.%Y%m%d"
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")

    assert expected_file.is_file()
    with open(expected_file) as f:
        assert "==MSG==" in f.read()


def test_loglevel(setup_test):
    """Test logvel."""
    (config, lab_name) = setup_test

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    config["rhtlab"]["logging"]["level"] = "WarNinG"
    labs.lablog.lablog_init(config, lab_name)
    logging.debug("==DEBUG MSG==")
    logging.info("==INFO MSG==")
    logging.warning("==WARNING MSG==")
    logging.error("==ERROR MSG==")
    logging.critical("==CRITICAL MSG==")

    assert expected_file.is_file()
    with open(expected_file) as f:
        content = f.read()
    assert "==DEBUG MSG==" not in content
    assert "==INFO MSG==" not in content
    assert "==WARNING MSG==" in content
    assert "==ERROR MSG==" in content
    assert "==CRITICAL MSG==" in content


def test_lognocapture(setup_test):
    """Test that stdout/stderr are not captured."""
    (config, lab_name) = setup_test

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")
    print("==STDOUT OUTPUT==")
    print("==STDERR OUTPUT==", file=sys.stderr)

    assert expected_file.is_file()
    with open(expected_file) as f:
        content = f.read()
    assert "==MSG==" in content
    assert "==STDOUT OUTPUT==" not in content
    assert "==STDERR OUTPUT==" not in content


def test_logcapture(setup_test):
    """Test that stdout/stderr are captured."""
    (config, lab_name) = setup_test

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    config["rhtlab"]["logging"]["capture_output"] = True
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")
    print("==STDOUT OUTPUT==")
    print("==STDERR OUTPUT==", file=sys.stderr)

    assert expected_file.is_file()
    with open(expected_file) as f:
        content = f.read()
    assert "==MSG==" in content
    assert "==STDOUT OUTPUT==" in content
    assert "==STDERR OUTPUT==" in content


def test_logcapturedebug(setup_test):
    """Test that stdout/stderr are captured when ``level`` is ``debug``."""
    (config, lab_name) = setup_test

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    config["rhtlab"]["logging"]["level"] = "Debug"
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")
    print("==STDOUT OUTPUT==")
    print("==STDERR OUTPUT==", file=sys.stderr)

    assert expected_file.is_file()
    with open(expected_file) as f:
        content = f.read()
    assert "==MSG==" in content
    assert "==STDOUT OUTPUT==" in content
    assert "==STDERR OUTPUT==" in content


def test_logcapturecmd(setup_test):
    """Test that the stdout/stderr of an external command are captured."""
    (config, lab_name) = setup_test

    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    config["rhtlab"]["logging"]["capture_output"] = True
    labs.lablog.lablog_init(config, lab_name)
    logging.critical("==MSG==")
    labs.lablog.run_capture(["cat", "DONOTEXIST", "/etc/hosts"])

    assert expected_file.is_file()
    with open(expected_file) as f:
        content = f.read()
    assert "==MSG==" in content
    assert "DONOTEXIST" in content
    # Assuming localhost is defined in /etc/hosts
    assert "localhost" in content


def remove_root_logger_handlers():
    """
    Removes all handlers from the root logger.

    This is required to test "lablog_init" from a clean state.
    """
    logger = logging.getLogger()
    logger.handlers = []
