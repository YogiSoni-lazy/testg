from unittest.mock import Mock

from labs.common.userinterface import Console
from labs import watch
from labs.core.step import LabStep
from labs.laberrors import LabError


def test__run_items():
    """
    Console(items).run_items() should run each item's task function,
    passing the item itself as the task parameter
    """

    def fail(item):
        item["done"] = True

    items = [
        {
            "label": "Test step",
            "task": fail
        }
    ]

    console = Console(items, spinner_delay=0)

    console.run_items()

    assert console.items[0]["done"] is True


def test__run_items__breaks_loop_on_fatal():
    """
    Console(items).run_items() should stop execution
    when a fatal step fails
    """
    step1 = Mock(side_effect=RuntimeError())
    step2 = Mock()

    items = [
        {
            "label": "Test step",
            "task": step1,
            "fatal": True
        },
        {
            "label": "Test step",
            "task": step2
        }
    ]

    try:
        Console(items, spinner_delay=0).run_items()
    except LabError:
        pass

    step1.assert_called_once()
    step2.assert_not_called()


def test__watch_labs():
    """
    Console accepts Lab watch steps
    """

    probe = Mock()

    @watch.watchstep("Some check")
    def check1():
        probe()
        return True

    console = Console(
        items=[],
        watch_items=[check1, check1, check1],
        spinner_delay=0
    )

    console.watch_lab()

    probe.assert_called()


def test__on__items__error__raise_error():
    """
    If run_items fails due to a failing fatal step,
    then Console should raise an exception and
    prevent the execution of "watch_lab"
    """

    probe = Mock()

    @watch.watchstep("Some check")
    def check1():
        probe()
        return True

    console = Console(
        # There is a fatal step that fails
        items=[LabStep(label="failing step", fatal=True, failed=True)],
        watch_items=[check1, check1, check1],
        spinner_delay=0
    )

    try:
        console.run_items().watch_lab()
    except LabError:
        pass

    probe.assert_not_called()
