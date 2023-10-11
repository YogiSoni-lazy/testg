"""
Functions to keep backwards compatiblity with old dicts/LabSteps
"""
import logging
from typing import Dict, List, Union

from .step import Step
from labs.laberrors import LabError
from labs.core.step import LabStep, step
from labs.core.task.runner import run_task


def run_steps(items: List[Union[Dict, LabStep]]):
    """Run a list of legacy item

    Args:
        items: a list of legacy items as dicts or a LabStep objects
    """
    for item in items:
        run_step(item)


def run_step(item: Union[Dict, LabStep]):
    """Run a legacy item

    Args:
        item: the legacy item as a dict or a LabStep object
    """
    item = step(item)

    if not item.label:
        raise LabError("The step does not include a label")

    with Step(item.label, fatal=item.fatal, grading=item.grading) as ctx:
        if item.has_task():
            ret_code = run_task(item)
        else:
            ret_code = 0

        failed = item.failed or ret_code

        if failed:
            ctx.add_error("The step has failed")

        for m in item.get_text_messages():
            ctx.add_message(m)

        if failed and item.fatal:
            msg = f"The '{item.label}' fatal step has failed"
            logging.error(msg)
            raise LabError(msg)
