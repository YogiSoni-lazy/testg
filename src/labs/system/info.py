import psutil
import socket
import platform
from typing import Dict


class SystemInfo:
    """
    Collects system information
    """
    _info: Dict

    def __init__(self):
        self._info = {}

    def collect(self):
        self.collect_info_cpu()
        self.collect_info_memory()
        self.collect_info_platform()
        self.collect_info_python()
        return self

    def collect_info_cpu(self) -> None:
        load_1, load_5, load_15 = psutil.getloadavg()
        self._info['cpu'] = {
            'count': psutil.cpu_count(),
            'load_average': {
                '1m': load_1,
                '5m': load_5,
                '15m': load_15,
            }
        }

    def collect_info_memory(self) -> None:
        self._info['memory'] = {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent
        }

    def collect_info_platform(self) -> None:
        self._info['platform'] = {
            'system': platform.system(),
            'release': platform.release(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
        }

    def collect_info_python(self) -> None:
        self._info['python'] = {
            'version': platform.python_version(),
            'compiler': platform.python_compiler(),
        }

    def get_info(self) -> Dict:
        return self._info
