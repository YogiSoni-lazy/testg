from json import dumps
from typing import Callable, Dict
from .info import SystemInfo

# A "Reporter" is a function that takes an instance of SystemInfo
# and generates a report
Reporter = Callable[[SystemInfo], None]


def json_reporter(sysinfo: SystemInfo):
    info = sysinfo.get_info()
    print(dumps(info, sort_keys=True, indent=4))


REPORTERS: Dict[str, Reporter] = {
    "json": json_reporter
}
