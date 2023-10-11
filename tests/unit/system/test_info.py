from unittest import TestCase
from unittest.mock import MagicMock, patch

from labs.system.info import SystemInfo


class TestSystemInfo(TestCase):
    @patch("psutil.getloadavg")
    @patch("psutil.cpu_count")
    def test_collect_info_cpu_succeeds(self, mock_cpu_count, mock_getloadvg):
        mock_cpu_count.return_value = 1
        mock_getloadvg.return_value = (1, 5, 15)

        system = SystemInfo()
        system.collect_info_cpu()

        expected = {
            'cpu': {
                'count': 1,
                'load_average': {
                    '1m': 1,
                    '5m': 5,
                    '15m': 15
                }
            }
        }

        self.assertDictEqual(expected, system.get_info())

    @patch("psutil.virtual_memory")
    def test_collect_info_memory_succeeds(self, mock_virtual_memory):
        mock_virtual_memory.return_value.total = 1
        mock_virtual_memory.return_value.available = 2
        mock_virtual_memory.return_value.used = 3
        mock_virtual_memory.return_value.percent = 4.5

        system = SystemInfo()
        system.collect_info_memory()

        expected = {
            'memory': {
                'total': 1,
                'available': 2,
                'used': 3,
                'percent': 4.5
            }
        }

        self.assertDictEqual(expected, system.get_info())

    @patch("socket.gethostname")
    @patch("platform.machine")
    @patch("platform.release")
    @patch("platform.system")
    def test_collect_info_platform_succeeds(self, mock_system, mock_release,
                                            mock_machine, mock_gethostname):
        mock_system.return_value = 'a-system'
        mock_release.return_value = 'a-release'
        mock_machine.return_value = 'an-arch'
        mock_gethostname.return_value = 'a-host'

        system = SystemInfo()
        system.collect_info_platform()

        expected = {
            'platform': {
                'system': 'a-system',
                'release': 'a-release',
                'architecture': 'an-arch',
                'hostname': 'a-host'
            }
        }

        self.assertDictEqual(expected, system.get_info())

    @patch("platform.python_compiler")
    @patch("platform.python_version")
    def test_collect_info_python_succeeds(self, mock_version, mock_compiler):
        mock_version.return_value = 'a-version'
        mock_compiler.return_value = 'a-compiler'

        system = SystemInfo()
        system.collect_info_python()

        expected = {
            'python': {
                'version': 'a-version',
                'compiler': 'a-compiler'
            }
        }

        self.assertDictEqual(expected, system.get_info())

    def test_collect_info_calls_substeps(self):
        system = SystemInfo()
        system.collect_info_cpu = MagicMock(return_value=None)
        system.collect_info_memory = MagicMock(return_value=None)
        system.collect_info_platform = MagicMock(return_value=None)
        system.collect_info_python = MagicMock(return_value=None)

        system.collect()

        assert system.collect_info_cpu.called
        assert system.collect_info_memory.called
        assert system.collect_info_platform.called
        assert system.collect_info_python.called
