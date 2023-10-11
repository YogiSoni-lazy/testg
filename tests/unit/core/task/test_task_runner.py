from unittest.mock import Mock, patch
from labs.core.step import step, LabStep
from labs.core.task.runner import run_task
from labs.common import steps
from labs.common import userinterface


@patch("labs.core.task.runner.logging")
def test__run_task__logs_exceptions(logging: Mock):
    """
    Console(items).run_items() should log exceptions
    """

    def fatal_error(item):
        raise RuntimeError("This is a fake error")

    item = step({
        "label": "Test step",
        "task": fatal_error
    })

    run_task(item)

    logging.exception.assert_called_once_with("Unexpected error")


def test__run_items__catches__exceptions():
    """
    Console(items).run_items() should catch raised Exception
    and set item["failed"] = True
    """

    def fatal_error(item):
        raise RuntimeError("This is a fake error")

    item = LabStep(
        label="Test step",
        task=fatal_error
    )

    run_task(item)

    assert item["failed"] is True


def test__run_items__catches__exceptions__and_add_messages():
    """
    Console(items).run_items() should catch raised Exception
    and add error messages
    """

    def fatal_error(item):
        raise RuntimeError("This is a fake error")

    item = step({
        "label": "Test step",
        "task": fatal_error
    })

    run_task(item)

    errors_text = " ".join([m["text"] for m in item["msgs"]])

    assert "error" in errors_text
    assert "This is a fake error" in errors_text
    assert "Check the log" in errors_text


def test__run_items__condition_works_well_with_steps():
    """
    Regression test a bug with conditions
    """
    items = [
        steps.run_command("foo", ["localhost"], "uptime")
    ]

    userinterface.Console(items, spinner_delay=0).run_items()


def test__run_items__positive_condition_works_well():
    """
    Conditions that evaluate to true are executed
    """

    # You might be wondering why "executed" is an array below, when we could
    # use a simple boolean. Well, that doesn't work:
    #
    # >>> executed = False
    # >>> def execute(item):
    # ...     executed = True
    # >>> execute(None)
    # >>> executed
    # False
    #
    # There's probably better ways to do this, but this is what I could come up
    # with quickly.

    executed = [False]

    def execute(item):
        executed[0] = True

    items = [
        {
            "task": execute,
            "label": "foo",
            "condition": lambda: True,
        }
    ]

    userinterface.Console(items, spinner_delay=0).run_items()

    assert executed[0]


def test__run_items__no_condition_works_well():
    """
    If no condition is used, things should always execute
    """

    executed = [False]

    def execute(item):
        executed[0] = True

    items = [
        {
            "task": execute,
            "label": "foo",
        }
    ]

    userinterface.Console(items, spinner_delay=0).run_items()

    assert executed[0]


def test__run_items__negative_condition_works_well():
    """
    Conditions that evaluate to false are not executed
    """

    executed = [False]

    def execute(item):
        executed[0] = True

    items = [
        {
            "task": execute,
            "label": "foo",
            "condition": lambda: False,
        }
    ]

    userinterface.Console(items, spinner_delay=0).run_items()

    assert not executed[0]
