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
import logging

from labs.grading import Default
from labs.common import labtools, userinterface

# List of hosts involved in that module. Before doing anything,
# the module checks that they can be reached on the network
_targets = [
    "localhost",
]


class ExerciseLogging(Default):
    """
    This is the DocString for the ExerciseLogging class
    """
    __LAB__ = "exercise-logging"

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.

    def start(self):
        """
        Prepare the system for starting the lab
        """
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
        logging.debug("Entering 'grade' function")
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
        if not items:
            logging.warning("'items' array is empty!")
        logging.debug("At 'grade' function, before 'ui'")
        ui = userinterface.Console(items)
        logging.debug("At 'grade' function, before 'run_items'")
        ui.run_items(action="Grading")
        logging.debug("At 'grade' function, before 'report_grade'")
        ui.report_grade()
        logging.debug("Leaving 'grade' function")

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
                "label": "Remove student's working directory",
                "task": self._finish_workdir,
            },
        ]
        userinterface.Console(items).run_items(action="Finishing")

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

    def _grade_test(self, item):
        """
        Check if test_file exists on ~/SKU/lab_name
        """
        logging.debug("Entering '_grade_test' function")
        lab_name = type(self).__name__
        logging.info("lab_name = %s", lab_name)
        file_path = os.path.join(
            labtools.get_sku_path(),
            lab_name,
            "test_file"
        )
        logging.info("file_path = %s", file_path)
        if not os.path.exists(file_path):
            item["failed"] = True
            item["msgs"] = [{"text": "File does not exist"}]
            logging.error(item["msgs"])
        logging.debug("Leaving '_grade_test' function")

    def _finish_workdir(self, item):
        """
        Remove student's working directory ~/SKU/lab_name
        """
        lab_name = type(self).__name__

        # Remove the ~/SKU/lab_name directory
        rmdir_result = labtools.rmdir(lab_name, recursive=True)
        if rmdir_result["failed"]:
            item["failed"] = True
            item["msgs"] = [{"text": "Directory could not be removed"}]
            return
