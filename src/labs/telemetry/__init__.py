"""
Entrypoint module for telemetry
"""
from typing import List

from . import upload, consent, config
from .session import NoTelemetry, TelemetrySession
from .config import is_enabled as is_telemetry_enabled


__all__ = ["upload", "consent", "start", "session", "config"]


def start(labconfig: dict, action: str = "", argv: List[str] = None):
    """
    Start a telemetry session and returns the instance
    The telemetry session is only created if:
    - the telemetry feature switch is on
    - the lab config contains telemetry.active True property
      (as a result of the user's consent to send telemetry)
    """

    labconfig_telemetry = labconfig.get("telemetry", {})
    telemetry_consent_given = labconfig_telemetry.get("active") is True

    if is_telemetry_enabled() and telemetry_consent_given:
        s = TelemetrySession(labconfig, action, argv)
    else:
        s = NoTelemetry()

    s.start()

    return s


session = start
