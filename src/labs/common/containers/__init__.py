"""
Utilities for containers and container-related tools
"""


import logging
import urllib3
from typing import Optional
from urllib3.exceptions import InsecureRequestWarning

import requests
from labs.common.commands import verify_command_succeeds

from labs.ui import Step
from labs.common.containers import podman


def check_registry_step(
    url: str,
    message: Optional[str] = None,
    expected_http_code=200,
    fatal=True,
    tls_verify=False
):
    """
    UI Step to verify that a container registry is up.
    By default, this step does not verify the TLS certificate of the server.

    Args:
        url: The url of the registry (must start with http or https)
        message: the Step message
        expected_http_code: HTTP response code to consider the check successful
        fatal: Flag to use a fatal step
        tls_verify: Flag to verify the TLS certificate of the server

    Returns:
        The step
    """
    # Do not show warnings when TLS is not verified
    urllib3.disable_warnings(InsecureRequestWarning)

    if not message:
        message = f"Verifying container registry at {url}"

    with Step(message, fatal=fatal) as step:
        try:
            response = requests.get(url, verify=tls_verify)
        except requests.exceptions.ConnectionError:
            logging.exception(f"Connection error to {url}")
            step.add_error(
                "A network error occurred while "
                f"connecting to registry at {url}. "
                f"Verify the registry URL and the network status."
            )
        except requests.exceptions.Timeout:
            logging.exception(f"Connection to {url} timed out")
            step.add_error(f"Connection to {url} timed out.")
        else:
            code = response.status_code
            if code != expected_http_code:
                step.add_error(
                    f"The container registry at {url} "
                    f"has returned an unexpected status code: {code}. "
                    f"Expected code: {expected_http_code}"
                )

    return step


def prune_images_step(message="Pruning images", fatal=True):
    """
    UI step to run 'podman image prune'

    Args:
        message: the Step message
        fatal: Flag to use a fatal step
    Returns:
        The step
    """
    with Step(message, fatal=fatal) as step:
        result = podman.prune_images()

        if not verify_command_succeeds(step, result):
            step.add_error("The 'podman image prune' command has failed")

    return step
