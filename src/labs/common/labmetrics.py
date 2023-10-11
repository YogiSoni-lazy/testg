import os
import time
import json
import tempfile
from functools import wraps
from typing import Any, Dict
from labs.grading import Default
from labs.labconfig import get_course_sku
from labs.common import labtools


def watch(lab: Default):

    """
    Decorator to gather metrics from a lab and save to a tempfile.

    This decorator is still a draft.
    For now, it can be used on subclasses of "labs.grading.Default"
    to gather basic metrics in a temporary file
    """

    original_start = lab.start
    original_finish = lab.finish

    @wraps(lab.start)
    def start(self, *args, **kwargs):
        result = original_start(self, *args, **kwargs)

        metrics = read_metrics(lab)
        metrics["start_time"] = time.time()
        save_metrics(lab, {"start_time": time.time()})

        return result

    @wraps(lab.finish)
    def finish(self, *args, **kwargs):
        result = original_finish(self, *args, **kwargs)

        metrics = read_metrics(lab)
        metrics["finish_time"] = time.time()
        save_metrics(lab, metrics)

        return result

    lab.start = start
    lab.finish = finish

    return lab


def read_metrics(lab: Default) -> Dict[str, Any]:
    filepath = get_metrics_filepath(lab)

    if not os.path.exists(filepath):
        labtools.mkdir(get_metrics_dir())
        save_metrics(lab, {})

    with open(filepath) as f:
        return json.load(f)


def save_metrics(lab: Default, metrics: Dict[str, Any]):
    filepath = get_metrics_filepath(lab)
    with open(filepath, "w") as f:
        json.dump(metrics, f)


def get_metrics_dir():
    return os.path.join(tempfile.gettempdir(), f"rht-{get_course_sku()}")


def get_metrics_filepath(lab):
    return os.path.join(get_metrics_dir(), f"{lab.__LAB__}.json")
