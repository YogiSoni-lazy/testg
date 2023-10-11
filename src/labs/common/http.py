"""
HTTP utilities
"""
import logging
from typing import Optional
import requests
from labs.ui import Step


def check_http_response_step(
    url: str,
    method="get",
    response_code_is=200,
    response_body_includes: Optional[str] = None,
    message: Optional[str] = None,
    verify_tls=False,
    grading=True,
    fatal=True
):
    """
    UI Step to verify the responses of HTTP requests

    :param url: The request URL
    :param method: The request method. "get" by default
    :param response_code_is: The expected response code. Default is 200
    :param response_body_includes: If provided, this parameter
                        must be a substring of the response body
    :param message: An optional step message
    :param verify_tls: Whether the request must verify the TLS certificates.
                        Default is False
    :param grading: Whether the step is a grading step. Default is True
    :param fatal: Whether the step is a fatal step. Default is True
    """

    message = message or f"Verifying response from {url}"

    with Step(message, grading, fatal) as step:
        try:
            response = make_request(url, method, verify_tls)
        except HttpRequestError as exception:
            return step.add_error(str(exception))

        code = response.status_code
        body = response.text

        if code != response_code_is:
            return step.add_error(
                f"{url} returned {code} status code. "
                f"Expected {response_code_is} "
            )

        if response_body_includes and response_body_includes not in body:
            expected_body_trimmed = response_body_includes[:10] + "..."
            return step.add_error(
                f"{url} response body does not "
                f"include '{expected_body_trimmed}'"
            )

        return step


def make_request(url: str, method="get", verify_tls=False):
    """
    Make a request to a URL and return a response

    The returned object is an instance of `requests.Response`
    (https://requests.readthedocs.io/en/latest/api/#requests.Response)

    If an error occurs, the exception is logged and
    the HttpRequestError exception is raised
    """
    response: Optional[requests.Response] = None
    try:
        response = requests.request(
            method=method, url=url, verify=verify_tls
        )
    except requests.exceptions.ConnectionError:
        _log_and_raise_error(f"Error connecting to {url}")
    except requests.exceptions.Timeout:
        _log_and_raise_error(f"Connection to {url} timed out")
    except requests.exceptions.RequestException:
        _log_and_raise_error(f"The request to {url} failed")
    else:
        code = response.status_code
        body = response.text
        logging.debug(
            f"HTTP {method} request to {url}. "
            f"Response code: {code}. "
            f"Response body: {body}"
        )
        return response


def _log_and_raise_error(error):
    logging.exception(error)
    raise HttpRequestError(error)


class HttpRequestError(Exception):
    pass
