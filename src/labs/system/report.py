"""
Facade module for generating a system report
"""

from .info import SystemInfo
from .reporters import REPORTERS


def generate(reporter="json"):
    """
    Generate a system info report
    """
    sysinfo = SystemInfo().collect()

    try:
        REPORTERS[reporter](sysinfo)
    except KeyError:
        raise ReporterNotFound


class ReporterNotFound(Exception):
    pass
