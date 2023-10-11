# Waiting for Conditions


To wait until a function that checks a condition returns a truthy value, use {py:func}`labs.common.utils.wait_until`:



``` python

from labs.common import utils

...

def start(self):

    with Step("Waiting for xyz") as step:
        ok = utils.wait_until(
            condition,
            sleep_seconds=1,
            max_wait=10 # seconds
        ):

        if not ok:
            step.add_error("condition is not met")


def condition():
    # check xyz and return a boolean
```

You can also check functions that accept arguments:

```python
def condition(x, y, z=1):
    return x + y == z

assert utils.wait_until(
        lambda: condition(2, -1),
        sleep_seconds=1,
        max_wait=10
    )

assert utils.wait_until(
        condition,
        sleep_seconds=1,
        max_wait=10,
        args=(2, -1)
    )

assert utils.wait_until(
        condition,
        sleep_seconds=1,
        max_wait=10,
        args=(2, 2),
        kwargs={"z": 4}
    )

assert utils.wait_until(
        condition,
        sleep_seconds=1,
        max_wait=10,
        kwargs={"x": 1, "y": 5, "z": 6}
    )

assert not utils.wait_until(
        condition,
        sleep_seconds=1,
        max_wait=10,
        args=(3),
        kwargs={"y": 0}
    )
```

## Changing Max Waiting Time Globally

If the `MULTIPLY_WAITS` environment variable is set, then `wait_until` multiplies `max_wait` by `MULTIPLY_WAITS`.

For example, assuming a `max_wait` value of 10 seconds.

* If `MULTIPLY_WAITS` is `0`, then `wait_until` does not wait.
* If `MULTIPLY_WAITS` is `1.5`, then `wait_until` waits for 15 seconds.

Students can use this variable to adjust lab scripts that require waits when their lab environment is not performing adequately.