#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.

"""
Grading module for GL007 Guided Exercise 2.

This module implements the start, grading, and finish actions.
"""

import os
import time

from labs.grading import Default
from labs.common import labtools, userinterface

# List of hosts involved in that module. Before doing anything,
# the module checks that they can be reached on the network
_targets = [
    "localhost",
]


class ExercisePython(Default):
    """
    This is the DocString for the ExercisePython class
    """
    __LAB__ = "exercise-python"

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.

    def start(self):
        """
        Prepare the system for starting the lab
        """
        # The items dictionary lists the tasks to run in order.
        # Each item describes a task. It is a dictionary with the following
        # keys:
        #     label: Short, one line description of the task.
        #      task: Method or function to run. If not set, or set to None,
        #            nothing is executed for that step.
        #    failed: This is the result of the task execution. The function
        #            defined by the "task" key must set that status to True or
        #            False. This status is used to display the completion
        #            status of the task.
        #      msgs: List of error messages. Those messages may be set by the
        #            "task" function when the task fails. They are
        #            displayed to provide additional information to students.
        #            Each message in the list is a dictionary with the key
        #            set to "text" and the text message as a value.
        #            For example:
        #              { "text": "The system cannot be reached"}
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            {
                "label": "Create a test file",
                "task": self._start_conf_deployed,
            },
            {
                "label": "Task that succeeds",
                "task": self._start_sample_success_task,
            },
            {
                "label": "Task that fails",
                "task": self._start_sample_failure_task,
            },
            {
                "label": "Do nothing task that always succeeds",
                "failed": False,
            },
            {
                "label": "Do nothing task that always fails",
                "failed": True,
            },
        ]
        userinterface.Console(items).run_items(action="Starting")

    def grade(self):
        """
        Perform evaluation steps on the system
        """
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            {
                "label": "Check test_file",
                "task": self._grade_test,
            },
        ]
        ui = userinterface.Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()

    def finish(self):
        """
        Perform post-lab cleanup
        """
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            {
                "label": "Remove lab files",
                "task": labtools.delete_workdir,
                "lab_name": self.__LAB__,
                "fatal": True
            },
        ]
        userinterface.Console(items).run_items(action="Finishing")

    ###########################################################################
    # Start tasks

    def _start_conf_deployed(self, item):
        """
        Create a sample file in ~/SKU/lab_name
        """
        lab_name = type(self).__name__
        student_working_dir = os.path.join(
            labtools.get_sku_path(),
            lab_name
        )

        # Create the ~/SKU/lab_name directory with a wrapper function
        mkdir_result = labtools.mkdir(student_working_dir)
        if mkdir_result["failed"]:
            item["failed"] = True
            item["msgs"] = [{"text": "Directory could not be created"}]
            return

        # Create a test_file inside ~/SKU/lab_name with native Python code
        file_path = os.path.join(
            student_working_dir,
            "test_file"
        )
        file_content = "Hello World!" + "\n"
        try:
            with open(file_path, 'w+') as file:
                file.write(file_content)
            item["failed"] = False
        except Exception:
            item["failed"] = True
            item["msgs"] = [
                {"text": "Can't write to file: {}".format(file_path)}
            ]
            return

    def _start_sample_success_task(self, item):
        item["failed"] = False
        time.sleep(1)

    def _start_sample_failure_task(self, item):
        item["failed"] = True
        item["msgs"] = [
            {"text": "Sample explanation of failure"},
            {"text": "Further explanation would go here"},
        ]
        time.sleep(1)

    ###########################################################################
    # Grading tasks

    def _grade_test(self, item):
        """
        Check if test_file exists on ~/SKU/lab_name
        """
        lab_name = type(self).__name__
        file_path = os.path.join(
            labtools.get_sku_path(),
            lab_name,
            "test_file"
        )
        if not os.path.exists(file_path):
            item["failed"] = True
            item["msgs"] = [{"text": "File does not exist"}]

    ###########################################################################
    # Finish tasks

    # (none)
