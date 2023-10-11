import datetime

import pytest
from labs.common import utils


def test__wait_until__happy():
    """
    wait_until() returns True if condition is met
    """

    def condition():
        return True

    assert utils.wait_until(
        condition, sleep_seconds=0, max_wait=0
    )


def test__wait_until__failure():
    """
    wait_until() returns False if condition is not met
    (max_wait in seconds)
    """

    def condition():
        return False

    assert not utils.wait_until(
        condition, sleep_seconds=0, max_wait=0
    )


def test__wait_until__failure__time_delta():
    """
    wait_until() returns True if condition is met
    (max_wait is set as timedelta)
    """

    def condition():
        return False

    assert not utils.wait_until(
        condition, sleep_seconds=0, max_wait=datetime.timedelta(seconds=0)
    )


def test__wait_until__wrong_max_wait_type():
    """
    wait_until() raises a type error if max_wait is not either:
    - datetime.timedelta
    - int
    """

    def condition():
        return False

    with pytest.raises(TypeError):
        utils.wait_until(
            condition, sleep_seconds=0, max_wait=1.5
        )


def test__wait_until__with_parameters():
    """
    wait_until() can verify functions that accept parameters
    """

    def condition(x, y, z=1):
        return x + y == z

    assert utils.wait_until(
            lambda: condition(2, -1),
            sleep_seconds=0,
            max_wait=0
        )

    assert utils.wait_until(
            condition,
            sleep_seconds=0,
            max_wait=0,
            args=(2, -1)
        )

    assert utils.wait_until(
            condition,
            sleep_seconds=0,
            max_wait=0,
            args=(2, 2),
            kwargs={"z": 4}
        )

    assert utils.wait_until(
            condition,
            sleep_seconds=0,
            max_wait=0,
            kwargs={"x": 1, "y": 5, "z": 6}
        )

    assert not utils.wait_until(
            condition,
            sleep_seconds=0,
            max_wait=0,
            args=(3),
            kwargs={"y": 0}
        )
