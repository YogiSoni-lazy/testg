import os
import time
import logging
import datetime
from typing import Callable, Optional, Union


def wait_until(
    condition: Callable[..., bool],
    sleep_seconds: int,
    max_wait: Union[datetime.timedelta, int],
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    """
    Wait until a condition returns a truthy value.

    If the `MULTIPLY_WAITS` environment variable is set,
    `max_wait` is multipled by this value.
    For example, if `MULTIPLY_WAITS=1.5` and `max_wait=10`,
    the actual max waiting time is 15 seconds.
    The same logic works for timedeltas.

    Args:
        condition: a callable that returns a truthy value on success.
        sleep_seconds: seconds to wait between retries.
        args: arguments to pass to the condition function.
        kwargs: keyword arguments to pass to the condition function.
        max_wait: maximum waiting time before considering
                  the condition as failed.
                  You can pass seconds (as an int value)
                  or an instance of datetime.timedelta

    Returns:
        True if the condition is met, False otherwise
    """
    start = datetime.datetime.now()

    if isinstance(max_wait, datetime.timedelta):
        max_wait_timedelta = max_wait
    elif isinstance(max_wait, int):
        max_wait_timedelta = datetime.timedelta(seconds=max_wait)
    else:
        raise TypeError(
            "Invalid max_wait. "
            "Use datetime.timedelta or int (seconds)"
        )

    multiplier = float(os.getenv("MULTIPLY_WAITS", "1"))
    logging.debug(f"Original max_wait: {max_wait_timedelta}")
    max_wait_timedelta *= multiplier
    logging.debug(
        f"Adjusted max_wait {max_wait_timedelta} ({multiplier} multiplier)"
    )

    args = args or ()
    kwargs = kwargs or {}

    while True:
        try:
            # Future improvement:
            # If condition doesn't return,
            # then the max wait time will not take effect.
            value = condition(*args, **kwargs)
            logging.debug(f"Executed condition, result was {value}")
            if value:
                return True
        except Exception as e:
            logging.error("Error invoking condition %s", e)

        elapsed = datetime.datetime.now() - start
        logging.debug(f"Elapsed {elapsed} - Max wait {max_wait_timedelta}")

        if elapsed > max_wait_timedelta:
            return False

        time.sleep(sleep_seconds)
