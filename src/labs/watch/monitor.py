"""
The "monitor" module
watches the exercise by running checks in an infinite loop
"""
import logging
from time import sleep
from typing import Callable, List, Optional
from inspect import getmembers
from .watchstep import is_watchstep, LabWatchStep, LabWatchStepFailure
from .reporter.base import WatchReporter
from .round import WatchRoundResults


class LabProgressMonitor:

    """
    Watches a lab by executing a set of watch steps.
    Each of these watch steps executes a verification of the lab progress.
    """

    watchsteps: List[LabWatchStep]
    sleep_seconds: int
    reporter: WatchReporter
    finish_fn: Optional[Callable[[], None]]

    def __init__(
        self,
        watchsteps: List[LabWatchStep],
        sleep_seconds=1,
        reporter=WatchReporter,
        on_finish: Optional[Callable[[], None]] = None,
    ):
        self.watchsteps = watchsteps
        self.sleep_seconds = sleep_seconds
        self.reporter = reporter
        self.finish_fn = on_finish

    @classmethod
    def with_checks_from(cls, module, **kargs):
        """
        Create from all the LabWatchSteps found in a module
        """
        watchsteps = [func for _, func in getmembers(module, is_watchstep)]
        return cls(watchsteps, kargs)

    def watch(self):
        """
        Watch the exercise by running the checks
        """
        results = self._run_watch_round()
        self.reporter.report(results)

        while not results.done():
            sleep(self.sleep_seconds)

            next = self._run_watch_round()

            if next != results:
                self.reporter.report(next)

            results = next

        self.finish()

    def _run_watch_round(self) -> WatchRoundResults:
        """
        Run the watch steps funcions once.
        Returns True if all checks pass.
        """
        results = WatchRoundResults()

        for step in self.watchsteps:
            try:
                step()
                results.add_success(step.label)

            except LabWatchStepFailure as error:
                results.add_error(step.label, error)
                logging.exception(f"[Watch step failed] {step.label}")

            except Exception as error:
                results.add_error(
                    step.label,
                    LabWatchStepFailure(
                        f"Exception catched: {error}",
                        hints=[
                            "Inspect the log file to find the stack trace"
                        ]
                    ))
                logging.exception(f"[Watch step exception] {step.label}")

        return results

    def finish(self):
        """
        Finish the lab monitorization.
        """
        self.reporter.success()

        if self.finish_fn and self.reporter.finish():
            self.finish_fn()
