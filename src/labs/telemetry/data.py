# I wish I could use Data Classes (Python >= 3.7),
# but we still have to support Python 3.6
# I also think there's a polyfill out there...


from datetime import datetime


class TelemetryReport:

    sku: str
    action: str
    started_at: datetime
    finished_at: datetime
    sysinfo: dict

    def __init__(self, sku, action, started_at, finished_at, sysinfo):
        self.sku = sku
        self.action = action
        self.started_at = started_at
        self.finished_at = finished_at
        self.sysinfo = sysinfo

    @property
    def duration(self):
        return self.finished_at - self.started_at

    def __str__(self):
        return (
            "TELEMETRY "
            f"| {self.sku} "
            f"| {self.action} "
            f"| {self.duration.total_seconds()}s"
            f"| {self.started_at}-{self.finished_at}"
        )

    def to_dict(self):
        return {
            **self.__dict__,
            "duration": self.duration.total_seconds()
        }
