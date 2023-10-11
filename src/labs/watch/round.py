from typing import List, NamedTuple
from .watchstep import LabWatchStepFailure


class StepResult(NamedTuple):
    """
    The result of running a "watch step"
    """
    ok: bool
    description: str
    error: LabWatchStepFailure


class WatchRoundResults:
    """
    The result of running a list of "watch steps" once.
    This is also called a "watch round"
    """

    items: List[StepResult]
    passing: int
    failing: int

    def __init__(self):
        self.items = []
        self.passing = 0
        self.failing = 0

    def __eq__(self, other: "WatchRoundResults") -> bool:
        if len(self.items) != len(other.items):
            return False

        for i, item in enumerate(self.items):
            if not (
                item.ok == other.items[i].ok and
                item.description == other.items[i].description and
                str(item.error) == str(other.items[i].error)
            ):
                return False

        return (self.passing == other.passing and
                self.failing == other.failing)

    def add_success(self, description: str):
        r = StepResult(True, description, None)
        self.items.append(r)
        self.passing += 1

    def add_error(self, description: str, error: LabWatchStepFailure):
        r = StepResult(False, description, error)
        self.items.append(r)
        self.failing += 1

    def done(self):
        """
        A watch round, and therefore the lab,
        is considered as complete when there are no failing steps.

        Note that if we invoke "watch" without any steps,
        this also returns True.
        """
        return self.failing == 0
