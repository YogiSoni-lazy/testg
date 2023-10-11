
import pytest
from labs.ui import Step, GradingStep
from labs.ui.step import StepFatalError


# Completeness and success

def test__step_context__is_done():
    """
    Step.is_done() is a boolean
    """
    with Step("test") as step:
        pass

    assert step.is_done() is True


def test__step_context__has_succeeded():
    """
    Step.has_succeeded() is true if the step has been set as ok
    """
    with Step("test") as step:
        step.ok()

    assert step.has_succeeded()


def test__step_empty_context__has_succeeded():
    """
    Step.has_succeeded() is true by default after
    a context manager ends
    """
    with Step("test") as step:
        pass

    assert step.has_succeeded()


def test__step__has_not_succeeded_if_not_ended():
    """
    Step.has_succeeded() is False if the step has not ended
    """
    step = Step("test").start()

    assert not step.has_succeeded()


# Explicit Failures

def test__step_contextfail___non_fatal():
    """
    Step.fail() marks a step as failed
    """
    with Step("test", fatal=False) as step:
        step.fail()

    assert step.has_failed()


def test__step_contextfail___fatal():
    """
    When the step is fatal,
    Step.fail() marks a step as failed and throws an exception
    """
    with pytest.raises(StepFatalError):
        with Step("test", fatal=True) as step:
            step.fail()

        assert step.has_failed()


def test__fatal_step_fail__raises_exception():
    """
    When the step is fatal,
    Step.fail() marks a step as failed and throws an exception

    (non-context-manager version)
    """
    step = Step("test", fatal=True)

    with pytest.raises(StepFatalError):
        step.fail().end()

    assert step.has_failed()


def test__step___add_error():
    """
    Step.add_error() marks a step as failed
    """

    with Step("test", fatal=False) as step:
        step.add_error("Hey this is an error")

    assert step.has_failed()


def test__step___add_errors():
    """
    Step.add_errors() adds multiple errors
    """

    with Step("test", fatal=False) as step:
        step.add_errors(["Error 1", "Error 2"])

    assert step.secondary_messages == ["Error 1", "Error 2"]


def test__fatal_step___add_error():
    """
    When the step is fatal,
    Step.add_error() marks a step as failed and throws an exception
    """
    with pytest.raises(StepFatalError):
        with Step("test", fatal=True) as step:
            step.add_error("Hey this is an error")

        assert step.has_failed()


def test__fatal_step___adds_messages():
    """
    Step.add_error() adds a message to the step secondary messages
    """

    with Step("test", fatal=False) as step:
        step.add_error("Hey this is an error")

    assert "Hey this is an error" in step.secondary_messages


# Failures Caused By Unhandled Exceptions

def test__step_fail__does_not_raise_expections():
    """
    A non-fatal Step context manager does not propagate exceptions
    but marks the step as failed.
    """
    with Step("hello", fatal=False) as step:
        raise RuntimeError("Some error happened")

    assert step.has_failed()


def test__step__progagates_exceptions():
    """
    A FATAL Step context manager DOES propagate exceptions
    AND marks the step as failed.
    """
    with pytest.raises(StepFatalError) as exc_info:
        with Step("hello", fatal=True) as step:
            raise RuntimeError("Some error happened")

        assert step.has_failed()
    assert exc_info.type == StepFatalError


# Normal Steps

def test__step__is_fatal_by_default():
    step = Step("test")
    assert step.is_fatal


# Grading Steps

def test__grading_step():
    step = GradingStep("test")
    assert step.is_grading


def test__grading_step__is_non_fatal_by_default():
    step = GradingStep("test")
    assert not step.is_fatal
