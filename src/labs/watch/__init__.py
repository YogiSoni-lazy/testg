"""
Lab Watch: Lab Progress Monitoring

This module watches any lab progress by using a list of check functions.
Check funcions should use the "@check" decorator
and the "expect" function for assertions, as follows:
"""
import os
from typing import Callable, List, Optional
from .monitor import LabProgressMonitor
from .watchstep import LabWatchStep, watchstep, expect, LabWatchStepFailure
from . import reporter


def watch(
    watchsteps: List[LabWatchStep],
    message="",
    sleep_seconds=1,
    finish: Optional[Callable[[], None]] = None,
):
    """
    Watches the progress made in a lab by executing a list of checks,
    called "watch steps"
    """
    monitor = LabProgressMonitor(
        watchsteps,
        sleep_seconds,
        resolve_reporter(message),
        finish
    )
    monitor.watch()
    return monitor


def resolve_reporter(message: str) -> reporter.WatchReporter:
    name = os.environ.get("WATCH_REPORTER", "").lower()

    return reporter.silent() if name == "silent" else reporter.console(message)


__all__ = ["watch", "watchstep", "expect", "LabWatchStepFailure"]
