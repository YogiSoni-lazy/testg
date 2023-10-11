import logging

from labs.core.step import LabStep


def run_task(step: LabStep):
    """
    Run a LabStep task function
    """
    ret_code = 0

    logging.info(f"[Task running] Item: {step}")

    try:
        ret_code = step.task(step)
    except Exception as e:
        logging.exception("Unexpected error")
        step.fail()
        step.add_message(f"An unexpected error ocurred: {e}")
        step.add_message("Check the log file for more details")

    logging.info(f"[Task completed] Code: {ret_code}, Item: {step}")

    return ret_code
