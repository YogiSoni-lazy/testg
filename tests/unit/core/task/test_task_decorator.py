from unittest import TestCase
from labs.core.task import task, TaskFailure, TaskException, TaskSuccess


class TestTaskDecorator(TestCase):

    """
    @task decorator
    """

    def test__return__none__succeeds(self):
        """
        A funcion decorated with @task
        is considered sucessful if the function
        does not return anything
        """

        @task
        def dummy():
            pass

        mytask = dummy()
        item = {}
        mytask(item)

        assert "failed" not in item

    def test__throw_raise_taskexception__causes_fatal(self):
        """
        A funcion decorated with @task
        fails if the function
        raises a TaskException
        """

        @task
        def dummy():
            raise TaskException("error")

        mytask = dummy()
        item = {}
        mytask(item)

        assert item["failed"] is True

    def test__returning_tasksuccess(self):
        """
        A funcion decorated with @task
        is succeeds if the function returns
        TaskSuccess
        """

        @task
        def dummy():
            return TaskSuccess()

        mytask = dummy()
        item = {}
        mytask(item)

        assert "failed" not in item

    def test__returning_taskfailure(self):
        """
        A funcion decorated with @task
        fails if the function returns
        TaskFailure
        """

        @task
        def dummy():
            return TaskFailure()

        mytask = dummy()
        item = {}
        mytask(item)

        assert item["failed"] is True
