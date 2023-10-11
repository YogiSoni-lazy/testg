from labs import watch
from labs.watch.reporter.console import (
    echo_failing_step, echo_passing_step
)


def test__echo_passing_test__receives_test_number_and_description():
    echo_passing_step("test1", 1)


def test__echo_failing_test__receives_assertion_error():
    error = watch.LabWatchStepFailure("Error", "Do xyz")
    echo_failing_step("test1", 1, error)
