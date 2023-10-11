
from abc import ABC
from functools import wraps
from typing import Dict, List,  Callable, Union

"""
@task decorator definition below
A function decorated with @task defines its signature
using regular Python parameters, instead of a dict.
This is to avoid errors caused by wrong dictionaries,
and to take advantage of intellisense and Python type hints.
Instead of defining a lab step like...
    {
        "label": "Step 1",
        "task": mytask
        "arg1": ...
        "arg2": ...
    }
...we define it as:
    {
        "label": "Step 1",
        "task": mytask(arg1, arg2)
    }
"""


class TaskException(Exception):
    msgs = []

    def __init__(self, msgs: Union[str, List[str]]):
        if isinstance(msgs, str):
            self.msgs = [msgs]
        else:
            self.msgs = msgs

        self.msgs = [{"text": msg} for msg in self.msgs]


class TaskResult(ABC):

    """
    Each task funcion should return an instance
    of this ABC (Abstract base class)
    """

    ok: bool
    msgs: List[str]

    def __init__(self, ok: bool, msgs: List[str] = None):
        self.ok = ok
        self.msgs = msgs or []

    def msgs_as_dicts(self):
        return [{"text": msg} for msg in self.msgs]


class TaskSuccess(TaskResult):

    def __init__(self, msgs: List[str] = None):
        return super().__init__(True, msgs)

    def __bool__(self):
        return True


class TaskFailure(TaskResult):

    def __init__(self, msgs: List[str] = None):
        return super().__init__(False, msgs)

    def __bool__(self):
        return False


TaskReturnValue = Union[TaskResult, bool, None]


def task(func: Callable[..., TaskReturnValue]):

    """
    This decorator wraps the call to the original function
    by accepting an "item" dictionary
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        def task(item: Dict):
            """
            This is the task function executed by DynoLabs, as:
                item["task"](item)
            """

            try:
                result = func(*args, **kwargs)

                # If the function returns False, raise error
                if result is False:
                    raise TaskException("")

                # If the function returns an instance of TaskResult
                # we parse the status and the msgs
                if isinstance(result, TaskResult):
                    if result.ok:
                        item["msgs"] = result.msgs_as_dicts()
                    else:
                        raise TaskException(result.msgs)

                # Otherwise, consider the function result sucessful
                # (as long as the function does not raise a TaskException)

            except TaskException as error:
                item["failed"] = True
                if "msgs" not in item:
                    item["msgs"] = []
                for m in error.msgs:
                    item["msgs"].append(m)

        return task

    return wrapper
