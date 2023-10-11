from labs.grading import Default
from labs.common.userinterface import Console


class ClassicGradingTest(Default):
    __LAB__ = "test-python-classic_grading"

    def grade(self):
        items = []
        ui = Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()
