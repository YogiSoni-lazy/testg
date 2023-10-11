import os
import requests
import logging
from typing import Callable

from labs.telemetry.data import TelemetryReport
from labs.telemetry import config

# A telemetry uploader is just a function
# that sends the telemetry data somewhere
TelemetryUploader = Callable[[TelemetryReport], None]


# Uploader strategies here vvvvv


def console_uploader(data: TelemetryReport):
    """
    Do not upload data, just log to console
    """
    print(data)


def http_uploader(data: TelemetryReport):
    """
    HTTP uploader that sends a POST request
    """
    # We don't want users to wait too much
    timeoutseconds = 3

    try:
        requests.post(
            config.get_api_endpoint(),
            json=data.to_dict(),
            timeout=timeoutseconds
        )
    except requests.exceptions.RequestException:
        # Telemetry upload errors should not modify the user experience
        # so let's catch everything and log the exception
        logging.exception("Error while uploading telemetry")


# There's a default uploader, but
# developers might want to use another one

uploaders = {"console": console_uploader, "http": http_uploader}

# TODO: use http as default
uploader_id = os.environ.get("TELEMETRY_UPLOADER", config.get_uploader())
_uploader: TelemetryUploader = uploaders[uploader_id]


def use(uploader: TelemetryUploader):
    """
    Define the uploader strategy to use
    """
    global _uploader
    _uploader = uploader


def send(data: TelemetryReport):
    """
    Upload/send data with the default uploader
    """
    _uploader(data)
