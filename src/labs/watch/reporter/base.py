from abc import ABC, abstractmethod
from ..round import WatchRoundResults


class WatchReporter(ABC):
    """
    Outputs the result of watching a lab
    """

    @abstractmethod
    def report(self, results: WatchRoundResults) -> None:
        """
        Reports watch round results
        """
        pass

    @abstractmethod
    def success(self) -> None:
        """
        Reports the lab sucess
        """
        pass

    @abstractmethod
    def finish(self) -> bool:
        """
        Reports and confirms whether "lab finish" should be run"
        """
        pass
