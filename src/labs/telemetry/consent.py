from uuid import uuid4

import click

from labs import labconfig
from . import config as telemetry_config


def ensure(labconfig_data: dict):
    """
    Ensure that the telemetry consent (yes/no) is saved in the labconfig file
    Only if the telemetry feature is switched on
    """
    telemetry_enabled = telemetry_config.is_enabled()
    telemetry_consent_configured = "telemetry" in labconfig_data

    if telemetry_enabled and not telemetry_consent_configured:
        _prompt_and_save(labconfig_data)


def _prompt_and_save(labconfig_data):
    # TODO: improve message
    consent = click.prompt(
        "Help us to improve RHT lab CLI by allowing it"
        " to collect anonymous usage data (Y/n)",
        default=False,
        show_choices=True,
        type=bool,
    )
    labconfig_data["telemetry"] = {"active": consent, "uuid": str(uuid4())}
    labconfig.savecfg(labconfig_data)
