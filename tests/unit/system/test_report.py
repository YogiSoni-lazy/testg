from unittest import TestCase
from unittest.mock import patch

from labs import system
from labs.system.report import ReporterNotFound


class TestSystemReport(TestCase):

    def test_report_fails_without_reporter_strategy(self):
        with self.assertRaises(ReporterNotFound):
            system.report.generate(None)

    @patch("labs.system.report.SystemInfo")
    @patch("labs.system.report.REPORTERS")
    def test_generate__calls_collect_info_and_strategy_send(
        self, REPORTERS, SystemInfo # noqa
    ):
        sysinfo = SystemInfo.return_value
        reporter = REPORTERS["json"]

        system.report.generate()

        assert sysinfo.collect.called
        assert reporter.called
