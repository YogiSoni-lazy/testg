from labs.grading import Default
from labs.common.userinterface import Console


class FailingPythonLabTest(Default):
    """
    Example Python lab script for integration tests
    (See rht-labs-core/tests dir)
    """

    __LAB__ = "test-python-lab-error"

    def start(self):
        """
        Prepare the system for starting the lab
        """

        items = [
            {
                "label": "Task that succeeds",
                "failed": True,
                "fatal": True
            },
        ]

        Console(items).run_items()
