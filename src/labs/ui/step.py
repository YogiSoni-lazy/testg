import logging
from enum import Enum
from typing import List

from halo import Halo
from click import echo, style

from labs import labconfig
from labs import lablog
from labs.ui.tools import format_message
from labs.ui._constants import BULLET, SECONDARY_MSG_PADDING, SPINNER


class StepResult(str, Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    PASS = "PASS"


class Step():

    """
    A UI step that starts with a message, shows a spinner,
    and finishes with a result
    """

    message: str
    is_grading: bool
    is_fatal: bool
    secondary_messages: List[str]

    def __init__(self, message: str, grading=False, fatal=True):
        self.message = message
        self.is_grading = grading
        self.is_fatal = fatal
        self.secondary_messages = []

        self._result = None
        self._secondary_message_padding = SECONDARY_MSG_PADDING
        self._spinner = Halo(
            text=self.message,
            spinner=SPINNER,
            enabled=not labconfig.is_dev_mode()
        )

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, _):
        if exc_type:
            logging.exception(f"Step '{self.message}' has failed. ")
            self.add_error(f"An unexpected error ocurred: {str(exc_value)}. ")
            self.add_error(f"Check {lablog._log_file.name} or use the "
                           "'lab logs' command for details.")

        self.end()

        if not self.is_fatal:
            # From the docs: If the method wishes to suppress the exception
            # (i.e., prevent it from being propagated),
            # it should return a true value
            return True

    def start(self):
        """
        Start the step by showing a spinner and the step message
        """
        self._spinner.start()
        return self

    def success(self):
        """
        Mark the step result as SUCCESS
        """
        if self.is_grading:
            self._result = StepResult.PASS
        else:
            self._result = StepResult.SUCCESS

        return self

    def ok(self):
        """
        Alias of success()
        """
        return self.success()

    def add_error(self, message: str):
        """
        Add an error message and mark the step as FAILED
        """
        self.add_message(message)
        self.fail()
        return self

    def add_errors(self, messages: List[str]):
        """
        Add multiple error messages and mark the step as FAILED
        """
        for message in messages:
            self.add_error(message)

    def fail(self):
        """
        Mark the step as FAILED
        """
        self._result = StepResult.FAIL
        return self

    def end(self):
        """
        Finish the step and prints the result.
        If the step is fatal, raises a StepFatalError
        """
        # If no result has been set at the end
        # we show success by default
        if not self.is_done():
            self.ok()

        if self.has_failed() and self.is_fatal:
            self.add_message(style("Cannot continue lab script", fg="red"))

        self._print_result()

        if self.has_failed() and self.is_fatal:
            raise StepFatalError(self)

    def add_message(self, message: str):
        """
        Add a message to be printed when the step finishes
        """
        self.secondary_messages.append(message)

    def is_done(self):
        return self._result is not None

    def has_succeeded(self):
        return self.is_done() and not self.has_failed()

    def has_failed(self):
        return self._result == StepResult.FAIL

    def _print_result(self,):
        if self._result:
            self._stop_spinner_and_persist_message()
            self._print_secondary_messages()

    def _stop_spinner_and_persist_message(self):
        if self._result:
            label, message = self._format_step_result_message(self._result)
            self._spinner.stop_and_persist(label, message)

    def _format_step_result_message(self, result: StepResult):
        result_label = self._colorize_result_labels()
        result_label_length = max(
            [len(label) for label in result_label.values()]
        )
        result_label = result_label[result].ljust(result_label_length)
        formatted_message = style(self.message, bold=True)

        return result_label, formatted_message

    def _colorize_result_labels(self):
        result_label = {
            StepResult.SUCCESS: style(StepResult.SUCCESS, fg="green"),
            StepResult.PASS: style(StepResult.PASS, fg="blue"),
            StepResult.FAIL: style(StepResult.FAIL, fg="red")
        }
        return result_label

    def _print_secondary_messages(self):
        for message in self.secondary_messages:
            echo(self._format_secondary_msg(message))

    def _format_secondary_msg(self, message: str):
        return format_message(
            message,
            left_padding=" " * self._secondary_message_padding,
            bullet=BULLET
        )


class GradingStep(Step):
    """
    By default, a grading step is non fatal
    """
    def __init__(self, message: str, fatal=False):
        super().__init__(message, grading=True, fatal=fatal)

    # this class is a friendly wrapper so people can write with GradingStep()
    # instead of with Step(grading=True, fatal=False). But users can still
    # create grading steps using the Step class directly, so do not put any
    # additional code here, as it is not guaranteed that grading steps will
    # use this class


class StepFatalError(Exception):
    """
    Fatal steps raise this exception when they fail
    """
    step: Step

    def __init__(self, step: Step, message="A fatal step has failed"):
        self.step = step
        super().__init__(message)
