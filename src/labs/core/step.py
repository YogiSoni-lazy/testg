"""
Definition of a Lab step
"""
from collections.abc import MutableMapping
from typing import Any, Callable, Dict, List, Union

# Type definitions used in the LabStep class below
LabStepMessage = Dict[str, str]
Task = Callable[["LabStep"], Any]
Condition = Callable[[Any], bool]


class LabStep(MutableMapping):

    """
    A lab step (aka lab item).
    Lab scripts are sequences of lab steps.

    To create a lab step, provide a label or a header.
    Optionally pass a task, as a function that accepts a LabStep.
    Optionally pass a condition, as a funct predicate that returns a boolean.
    Also optionally indicate whether the step is fatal, a grading step,
    or only a header.

    You can add any other additional property to a lab step
    by passing it as a keyword parameter (**additional_props).

    A lab step is also an instance of MutableMapping,
    which means you can treat it as a dict.
    To access the attributes of lab steps, you can use:
        - Regular object-like (myobj.attr1)
        - Dict-like access (myobj["attr1"])
    """

    label: Union[str, None]
    task: Union[Task, None]
    condition: Condition
    fatal: bool
    grading: bool
    failed: bool
    header: Union[str, None]
    msgs: List[LabStepMessage]

    def __init__(
        self,
        label: Union[str, None] = None,
        task: Union[Task, None] = None,
        condition: Condition = lambda: True,
        fatal=False,
        grading=False,
        failed=False,
        header: Union[str, None] = None,
        msgs: List[LabStepMessage] = None,
        **additional_props
    ):
        if not (header or label):
            raise LabStepInitilizationError(
                "Lab steps require either a label or a header"
            )

        self.label = label
        self.task = task
        self.condition = condition
        self.fatal = fatal
        self.grading = grading
        self.failed = failed
        self.header = header
        self.msgs = msgs or []

        # Add all the other "additional_props" as object attributes.
        # The way to do this is by adding them to
        # the internal attributes dict (__dict__)
        self.__dict__.update(**additional_props)

    def fail(self):
        """
        Mark the lab step as failed
        """
        self.failed = True

    def is_header(self):
        """
        Whether the step is just a header
        """
        return self.header is not None

    def has_task(self):
        """
        Whether the step has a task to execute
        """
        return self.task is not None

    def add_message(self, text: str):
        """
        Add the specified text as a step message
        """
        self.msgs.append({"text": text})

    def get_text_messages(self):
        """
        Returns the "text" property of text messages.
        Only msgs including the "text" key are returned.
        """
        return [m["text"] for m in self.msgs if "text" in m]

    # Methods bellow implement the MutableMapping abstract class
    # MutableMapping capabilities allows dict-like access

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


def step(item: Union[Dict, LabStep]) -> LabStep:
    """
    Factory function to create a LabStep instance from a dict
    """
    # I am a bit concerned about this.
    #
    # For devs who pass a list of dictionaries,
    # this will create new instances of their steps.
    # The reference to the actual step object being executed will be hidden.
    #
    # Devs who pass a list of LabSteps instances
    # will keep the references to their steps
    return item if isinstance(item, LabStep) else LabStep(**item)


def ensure_labsteps(items: List[Union[Dict, LabStep]]):
    """
    Given a list of lab steps or dicts,
    ensure that all the elements are instances of LabStep.
    """
    return [step(i) for i in items]


class LabStepInitilizationError(Exception):
    pass
