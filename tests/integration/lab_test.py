import os
import json
import tempfile
import subprocess
from pathlib import Path
from subprocess import PIPE
from tests.testcourse.ts000.test_python_classic_grading import (
    ClassicGradingTest
)

import ts000.version
from click.testing import CliRunner
from src.labs import lab, version
from tests.testcourse.ts000.test_python_lab import PythonLabTest
from tests.testcourse.ts000.test_python_lab_error import FailingPythonLabTest


# lab select


def test__lab_select__creates_config_file():

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.yaml")
        env = {
            **os.environ.copy(),
            "RHT_LABS_CONFIG_PATH": config_path
        }

        output, error, returncode = _invoke_lab_method(
            "ts000", "select", env=env
        )

        assert returncode == 0, error
        assert Path(config_path).exists(), "config.xml file does not exist"


# lab start
# Requires the ts000 test course
# (see tests/_util/config.yaml, testcourse, and tests/conftest.py)


def test__lab_start__prints_common_messages():
    labname = PythonLabTest.__LAB__

    try:
        output, _, returncode = _invoke_lab_method(labname, "start")

        assert returncode == 0
        assert "Starting lab" in output
        assert "SUCCESS" in output
        assert "FAIL" in output
    except Exception as e:
        # Pytest captures stdout and only prints it if the test fails
        print(output)
        raise e


# lab fix
# Requires the ts000 test course
# (see tests/_util/config.yaml, testcourse, and tests/conftest.py)

def test_lab_fix__works():
    labname = PythonLabTest.__LAB__

    try:
        output, _, returncode = _invoke_lab_method(labname, "fix")

        assert returncode == 0
        assert "Fixing lab!" in output
        assert "SUCCESS" in output
    except Exception as e:
        # Pytest captures stdout and only prints it if the test fails
        print(output)
        raise e


def test__lab_start__returns__error_code__on_failure():
    labname = FailingPythonLabTest.__LAB__

    _, _, returncode = _invoke_lab_method(labname, "start")
    assert returncode == 1


def test_lab_start__uses_watch():
    labname = PythonLabTest.__LAB__

    output, _, returncode = _invoke_lab_method(labname, "start")

    assert returncode == 0
    assert "tracking lab" in output.lower()
    assert "successfully completed the exercise" in output


def test_lab_classic_grading__works():
    labname = ClassicGradingTest.__LAB__

    output, _, returncode = _invoke_lab_method(labname, "grade")

    assert returncode == 0
    assert "overall lab grade: pass" in output.lower()


def _invoke_lab_method(labname, method, env=None):
    # click.CliRunner is not capturing lab output,
    # so we fall back to the standard subprocess library
    result = subprocess.run(
        ["lab", method, labname],
        encoding="utf-8",
        stdout=PIPE,
        stderr=PIPE,
        env=env
    )

    return result.stdout, result.stderr, result.returncode


# lab system-info


def test_command__system_info__exit_code():
    runner = CliRunner()

    result = runner.invoke(lab.system_info)

    assert result.exit_code == 0


def test_command__system_info__output():
    runner = CliRunner()

    result = runner.invoke(lab.system_info)

    assert_output_is_sysinfo_report(result.output)


def assert_output_is_sysinfo_report(output: str):
    report = json.loads(output)

    assert report["cpu"]["count"] > 0

    assert "load_average" in report["cpu"]

    assert report["memory"]["total"] > 0

    assert report["platform"]["system"]

    assert report["python"]["version"]


# lab --version


def test_command__main__core_version():
    """
    lab --version
    should return the rht-labs-core version
    """
    runner = CliRunner()

    result = runner.invoke(lab.main, "--version")

    assert version.__version__ in result.output


def test_command__main__course_sku():
    """
    lab --version
    should return the rht-labs-sku in use
    """
    runner = CliRunner()

    result = runner.invoke(lab.main, "--version")

    assert "ts000" in result.output


def test_command__main__course_version():
    """
    lab --version
    should return the version of the rht-labs-sku in use
    """
    runner = CliRunner()

    result = runner.invoke(lab.main, "--version")

    assert ts000.version.__version__ in result.output


def test_command__main__course_version__no_course_set():
    """
    lab --version
    should warn that no course is set if the config file does not exist
    """
    runner = CliRunner()

    result = runner.invoke(
        lab.main,
        "--version",
        env={"RHT_LABS_CONFIG_PATH": "/dev/null"},
        catch_exceptions=False,
    )

    assert "no course" in result.output.lower()


# lab logs


def test_command__logs__no_error():
    """
    lab logs exits with 0 code
    """
    runner = CliRunner()

    result = runner.invoke(lab.main, "logs")

    assert result.exit_code == 0


def test_command__logs__missing_script__single_file():
    """
    Given: Configuration for logging to a single log file for all exercises

    When: 'lab logs none`

    Then: Exits sucesfully because the script name (none) is ignored
    """
    runner = CliRunner()

    result = runner.invoke(lab.main, "logs none")

    assert result.exit_code == 0


def test_command__logs__missing_script__multiple_files():
    """
    Given: Configuration for logging to a log file per exercise

    When: 'lab logs none`

    Then: Fails because the log file `none` does not exist
    """
    config_path = str(
        Path(__file__).parent.parent.joinpath("_util/config-log-to-dir.yaml")
    )

    runner = CliRunner()

    result = runner.invoke(
        lab.main,
        "logs none",
        env={"RHT_LABS_CONFIG_PATH": config_path},
    )

    assert "not exist" in result.stdout
    assert result.exit_code == 1


# Add tests for other commands below
# lab ...
