from .base import WatchReporter
from .console import ConsoleWatchReporter
from .silent import SilentWatchReporter

console = ConsoleWatchReporter
silent = SilentWatchReporter

__all__ = [WatchReporter, console, silent]
