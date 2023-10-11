from .base import WatchReporter
from ..round import WatchRoundResults


class SilentWatchReporter(WatchReporter):
    """
    A lab watch reporter that produces no output.
    Useful as a test dummy
    """
    def report(self, results: WatchRoundResults) -> None:
        pass

    def success(self) -> None:
        pass

    def finish(self) -> bool:
        return True
