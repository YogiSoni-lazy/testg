from unittest.mock import patch
from labs.ui import legacy


@patch("labs.ui.legacy.Step")
def test__legacy_grading_step__prints_pass(Step): # noqa

    legacy.run_step({
        "label": "A grading step",
        "fatal": False,
        "grading": True,
    })

    Step.assert_called_with("A grading step", fatal=False, grading=True)
