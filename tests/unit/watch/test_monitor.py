import sys
from types import FunctionType
from unittest.mock import Mock
from labs import watch
from labs.watch.monitor import LabProgressMonitor
from labs.watch.reporter.base import WatchReporter


def test__labprogressmonitor__uses_the_decorated_test_functions():
    current_module = sys.modules[__name__]
    monitor = LabProgressMonitor.with_checks_from(current_module)
    assert monitor.watchsteps == [dummy_test]


def test__labprogressmonitor_run_once__returns_success():
    test1 = mock_labtest()
    test2 = mock_labtest()
    monitor = LabProgressMonitor([test1, test2])
    results = monitor._run_watch_round()
    assert results.done()


def test__labprogressmonitor_run_once__returns_false_when_tests_fail():
    test1 = mock_labtest()
    test2 = mock_labtest(side_effect=watch.LabWatchStepFailure("error"))
    monitor = LabProgressMonitor([test1, test2])
    results = monitor._run_watch_round()
    assert not results.done()


def test__labprogressmonitor_watch__reports__success__when_tests_pass():
    test = mock_labtest()
    reporter = Mock(spec=WatchReporter)
    monitor = LabProgressMonitor([test], sleep_seconds=0, reporter=reporter)
    monitor.watch()
    reporter.success.assert_called()


def test__labprogressmonitor__calls_confirm_finish():
    test = mock_labtest()
    reporter = Mock(spec=WatchReporter)
    monitor = LabProgressMonitor(
        [test], sleep_seconds=0, on_finish=Mock(), reporter=reporter
    )
    monitor.watch()
    reporter.finish.assert_called()


@watch.watchstep("This is a dummy test")
def dummy_test():
    pass


def mock_labtest(*args, **kargs):
    mock = Mock(*args, spec=FunctionType, **kargs)
    return watch.watchstep("dummy")(mock)
