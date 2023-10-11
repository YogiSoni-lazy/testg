from contextlib import contextmanager
from datetime import datetime
from time import sleep
from unittest.mock import Mock, patch
from labs.telemetry.upload import http_uploader
from src.labs import telemetry


def test__telemetry_logs_start_time():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config) as session:
            pass

        # Then
        assert session.started_at <= datetime.now()


def test__telemetry_logs_finish_time():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config) as session:
            pass

        # Then
        assert session.finished_at >= session.started_at


def test__telemetry_logs_command_duration():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config) as session:
            pass

        # Then
        assert session.duration.total_seconds() > 0


def test__telemetry_logs_lab_action():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config, action="grade") as session:
            pass

        # Then
        assert session.action == "grade"


def test__telemetry_finish__logs_full_command():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(
            config, argv=["lab", "start", "xyz"]
        ) as session:
            pass

        # Then
        assert session.argv == ["lab", "start", "xyz"]


def test__telemetry_report_includes_sku():
    # Given
    with telementry_enabled_and_config() as config:

        config = given_lab_config()
        config["rhtlab"]["course"]["sku"] = "AD123"

        # When
        with telemetry.session(config) as session:
            pass

        # Then
        assert session.report.sku == "AD123"


def test__telemetry_includes_platform_system_info():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config) as t:
            pass

        # Then
        assert "platform" in t.report.sysinfo


def test__telemetry_includes_python_system_info():
    # Given
    with telementry_enabled_and_config() as config:

        # When
        with telemetry.session(config) as t:
            pass

        # Then
        assert "python" in t.report.sysinfo


def test__telemetry_calls_uploader():
    # Given
    with telementry_enabled_and_config() as config:
        uploader = fake_uploader()
        telemetry.upload.use(uploader)

        # When
        with telemetry.session(config, "start"):
            sleep(0.05)

        # Then
        assert_uploader_called_with_telemetry_data(uploader, action="start")


def test__telemetry__does_not_run_when_consent_not_given():
    # Given the student has not given telemetry consent
    # (so the telemetry.active lab config value is False)
    with telementry_enabled_and_config() as config:
        config["telemetry"]["active"] = False

        telemetry.upload.use(fake_uploader())

        # When
        with telemetry.session(config, "start") as t:
            pass

        # Then
        assert t.started_at is None


@patch("labs.telemetry.is_telemetry_enabled")
def test__telemetry__does_not_run_when_not_activated_at_pkg_level(
    is_telemetry_enabled
):
    # Given the telemetry feature is deactivated at the package level
    config = given_lab_config()
    is_telemetry_enabled.return_value = False

    telemetry.upload.use(fake_uploader())

    # When
    with telemetry.session(config, "start") as t:
        pass

    # Then
    assert t.started_at is None


@patch("labs.telemetry.upload.requests")
def test__telemetry_http_sends_a_post_request(requests):
    # Given
    with telementry_enabled_and_config() as config:
        telemetry.upload.use(http_uploader)

        # When
        with telemetry.session(config):
            pass

        # Then
        requests.post.assert_called_once()


def fake_uploader():
    return Mock()


def assert_uploader_called_with_telemetry_data(uploader, action):
    assert uploader.call_args[0][0].action == action
    assert uploader.call_args[0][0].duration.total_seconds() > 0


def given_lab_config():
    return {
        "rhtlab": {
            "course": {"sku": "ad482"},
            "logging": {"level": "error", "path": "/tmp/rht-logs"},
        },
        "telemetry": {
            "active": True,
            "uuid": "unique",
        },
    }


@contextmanager
def telementry_enabled_and_config():
    telemetry.upload.use(fake_uploader())

    with patch(
        "src.labs.telemetry.is_telemetry_enabled"
    ) as is_telemetry_enabled:
        is_telemetry_enabled.return_value = True
        yield given_lab_config()
