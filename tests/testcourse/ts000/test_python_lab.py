import sys
import logging
from labs.grading import Default
from labs import watch
from labs.common import steps
from labs.core.task import task, TaskFailure
from labs.common.userinterface import Console
from labs.ui.step import Step


class PythonLabTest(Default):
    """
    Example Python lab script for integration tests
    (See rht-labs-core/tests dir)
    """

    __LAB__ = "test-python-lab"

    def start(self):
        """
        Prepare the system for starting the lab
        """

        items = [
            {
                "label": "Task that succeeds",
                "task": sample_task(simulate_failure=False),
            },
            steps.header("Subheader example, task below fails"),
            {
                "label": "Task that fails",
                "task": sample_task(simulate_failure=True),
            },
            steps.header("Another subheader example, rest of tasks succeed"),
            {
                "label": "Do nothing task that always succeeds",
                "failed": False,
            },
            {
                "header": "Subheader example, task below fails",
            },
            {
                "label": "Do nothing task that always fails",
                "failed": True,
            },
            {
                "header": "Another subheader example, rest of tasks succeed",
            },
            {
                "label": "Copy exercise files",
                "task": lambda x: None,
                "lab_name": self.__LAB__,
                "fatal": True,
            },
        ]

        # -- Example of lab watch --
        #
        # The "watch" function watches the lab progress by continously
        # executing a list of checks.
        # The lab script finishes when all checks pass.
        # Check funcions must be decorated with "@watch.checkpoint"

        checkpoints = [
            checkpoint1,
            checkpoint2
        ]

        console = Console(items, watch_items=checkpoints)

        console.run_items()
        console.watch_lab()

    def fix(self):
        with Step("Fixing lab!"):
            ...


# -- A check used by lab watch --
#
# A check funcion requires:
# - The @check decorator, to set the description of the check
# - The use of "expect" to validate a condition
# - (Optional) An error message, shown if the check does not pass
# - (Optional) A list of hint messages, shown if the check does not pass
@watch.watchstep("Check file a.txt exists")
def checkpoint1():
    watch.expect(True)


@watch.watchstep("Check server is reachable")
def checkpoint2():
    watch.expect(True)


@task
def sample_task(simulate_failure: bool):
    logging.debug(sys._getframe().f_code.co_name)

    if simulate_failure:
        return TaskFailure(["I'm failing"])
