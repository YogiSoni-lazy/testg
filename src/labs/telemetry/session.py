from typing import List
from datetime import datetime

from .data import TelemetryReport
from .upload import send
from labs.system.info import SystemInfo

# TODO: read config to ignore telemetry if telemetry consent is not given


class TelemetrySession:
    """
    A telemetry session normally watches the execution of a single command
    """

    started_at: datetime
    finished_at: datetime
    sysinfo: dict
    action: str
    report: TelemetryReport
    argv: List[str]

    def __init__(
        self,
        config: dict,
        action: str = "",
        argv: List[str] = None,
    ) -> None:
        """
        action: Lab action, such as "grade" and "finish"
        """
        self.started_at = None
        self.finished_at = None
        self._config = config
        self.action = action
        self.argv = argv or []

    @property
    def duration(self):
        return self.finished_at - self.started_at

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.finish()

    def start(self):
        self.started_at = datetime.now()

    def finish(self):
        self.finished_at = datetime.now()

        self._build_report()

        send(self.report)

    def _build_report(self):
        system = SystemInfo()
        system.collect_info_platform(),
        system.collect_info_python()
        sysinfo = system.get_info()
        sku = self._config["rhtlab"]["course"]["sku"]

        self.report = TelemetryReport(
            sku,
            self.action,
            self.started_at,
            self.finished_at,
            sysinfo
        )


class NoTelemetry(TelemetrySession):
    """
    Use this when user does not accept the telementry consent
    """
    def __init__(self):
        super().__init__({}, None, None)

    def start(self):
        pass

    def finish(self):
        pass
