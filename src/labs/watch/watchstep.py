from typing import Any, Callable, List, Dict, Union


TestFunction = Callable[[], None]


class LabWatchStep:
    """
    A lab watch step is a verification performed during a lab watch session.
    The lab watch feature watches a list of LabWatchTest
    until all of them pass.

    Each LabWatchTest contains:
        - A label
        - A test function: Test functions do not accept parameters
          and return None.
    """

    label: str
    testfn: TestFunction

    def __init__(self, label: str, testfn: TestFunction):
        """
        Do not use this constructor,
        instead, use the @watchstep decorator
        """
        self.label = label
        self.testfn = testfn

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.testfn(*args, **kwds)


def watchstep(label: str) -> LabWatchStep:
    """
    Decorates a function to be a lab watch step.
    """
    def decorator(func):
        return LabWatchStep(label, testfn=func)

    return decorator


def is_watchstep(fn: Union[Callable, Dict]):
    """
    Check whether a function is a lab watch step
    """
    return isinstance(fn, LabWatchStep)


def expect(condition: bool, error="", hints: List[str] = []):
    """
    Expects a condition to be True in a LabWatchStep test
    If false, raises a LabWatchStepFailure with error_msg and hints

    This is a solution to avoid using the built-in "assert" expression.

    We don't want to use "assert".
    "assert" statements are ignored when python runs in optimized mode
    (__debug__ == False)
    https://docs.python.org/3.6/reference/simple_stmts.html#the-assert-statement
    """
    if not condition:
        raise LabWatchStepFailure(error or "Watch step failed", hints)


class LabWatchStepFailure(AssertionError):
    message: str
    hints: List[str]

    def __init__(self, message: str, hints: List[str] = []) -> None:
        self.message = message
        self.hints = hints
        super().__init__(message)
