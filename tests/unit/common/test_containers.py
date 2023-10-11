from pytest_subprocess import FakeProcess

from requests.exceptions import ConnectionError, Timeout
from requests_mock import Mocker as RequestMocker

from labs.common.containers import check_registry_step, prune_images_step


def test__check_registry_step__happy():
    """
    check_registry_step() is OK when registry is UP
    """
    url = "http://registry.example.com"

    with RequestMocker() as m:
        m.get(url, status_code=200)

        step = check_registry_step(url, fatal=False)

    assert step.has_succeeded()


def test__check_registry_step__bad_http_code():
    """
    check_registry_step() fails when registry returns a non-200 code
    """
    url = "http://registry.example.com"

    with RequestMocker() as m:
        m.get(url, status_code=500)

        step = check_registry_step(url, fatal=False)

    assert step.has_failed()
    assert "unexpected" in " ".join(step.secondary_messages)


def test__check_registry_step__connection_error():
    """
    check_registry_step() fails when there is a connection error
    """
    url = "http://registry.example.com"

    with RequestMocker() as m:
        m.get(url, exc=ConnectionError)

        step = check_registry_step(url, fatal=False)

    assert step.has_failed()
    assert "network error" in " ".join(step.secondary_messages)


def test__check_registry_step__timeout():
    """
    check_registry_step() fails when there is a timeout error
    """
    url = "http://registry.example.com"

    with RequestMocker() as m:
        m.get(url, exc=Timeout)

        step = check_registry_step(url, fatal=False)

    assert step.has_failed()
    assert "timed out" in " ".join(step.secondary_messages)


def test__prune_images__step(fp: FakeProcess):
    """
    prune_images_step() OK
    """
    fp.register(["podman", fp.any()])

    step = prune_images_step()

    assert step.has_succeeded()


def test__prune_images__failure(fp: FakeProcess):
    """
    prune_images_step() fails if command return non-zero code
    """
    fp.register(["podman", fp.any()], returncode=1)

    step = prune_images_step(fatal=False)

    assert step.has_failed()
    assert "podman image prune" in step.secondary_messages[2]
