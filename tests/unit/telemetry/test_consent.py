from unittest.mock import patch
from labs import telemetry


@patch("labs.telemetry.consent.click")
@patch("labs.telemetry.consent.labconfig")
@patch("labs.telemetry.consent.telemetry_config")
def test__telemetry_does_not_write_lab_config_if_disabled(
    telemetry_config, labconfig, click
):
    # Given Telemetry feature switch is disabled
    telemetry_config.is_enabled.return_value = False
    # and given any labconfig
    labcfg_data = {}

    # When
    telemetry.consent.ensure(labcfg_data)

    # Then
    click.prompt.assert_not_called()
    labconfig.savecfg.assert_not_called()


@patch("labs.telemetry.consent.click")
@patch("labs.telemetry.consent.labconfig")
@patch("labs.telemetry.consent.telemetry_config")
def test__telemetry_does_not_write_labconfig_if_consent_already_given(
    telemetry_config, labconfig, click
):
    # Given Telemetry feature switch is enabled
    telemetry_config.is_enabled.return_value = True
    # and given any labconfig
    labcfg_data = {
        "telemetry": {
            "active": False,
            "uuid": "unique",
        }
    }

    # When
    telemetry.consent.ensure(labcfg_data)

    # Then
    click.prompt.assert_not_called()
    labconfig.savecfg.assert_not_called()


@patch("labs.telemetry.consent.click")
@patch("labs.telemetry.consent.labconfig")
@patch("labs.telemetry.consent.telemetry_config")
def test__telemetry_consent_writes_labconfig(
    telemetry_config, labconfig, click
):
    # Given Telemetry feature switch is enabled
    telemetry_config.is_enabled.return_value = True
    # and given a labconfig with no telementry config
    labcfg_data = {}

    # When
    telemetry.consent.ensure(labcfg_data)

    # Then user is prompted for consent and lab config is saved
    click.prompt.assert_called_once()
    labconfig.savecfg.assert_called_once()
