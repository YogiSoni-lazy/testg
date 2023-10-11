#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#
# CHANGELOG
# * Sep 28 2020 Your Name <yname@redhat.com>
#   - original code

"""
Grading module for RH000 LAB_OR_GE_TITLE guided exercise (or lab).

This module either does start, grading, or finish for the
LAB_OR_GE_TITLE guided exercise (or lab).
"""

###############################################################################
#   How to use this template:
#
# 1. Save the file as chapter-keyword.py, don't use WordCaps or camelCase
# 2. Adjust the CHANGELOG and docstring above.
# 3. Define the hosts that are used in this activity in the _targets list.
# 4. Rename the class using WordCaps
# 5. Set the __LAB__ variable to match the file name
#    (without the .py extension)
# 6. Remove the methods that your lab script does not support.
#    start, finish, or grade
# 7. Remove these "How to use this template" comments
###############################################################################

# FIXME: Catching too general exception 'Exception' (broad-except)

import os
import random
import sys
import stat
import time
import logging
import subprocess

from labs import labconfig
from labs.grading import Default
from labs.common import labtools, userinterface, steps
from labs.lab import LabError


# Course SKU
SKU = labconfig.get_course_sku().upper()

# List of hosts involved in that module. Before doing anything,
# the module checks that they can be reached on the network
_targets = [
    "localhost",
    # "server-a",
    # "server-b",
    # "classroom",
    # "bastion",
]


# Change the class name to match your file name with WordCaps
class ExamplePython(Default):
    """
    Example Python lab script for GL006
    """
    __LAB__ = "example-python"

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.

    def start(self):
        #######################################################################
        #   How to use this template:
        #
        # The items dictionary lists the tasks to run in order.
        # Each item describes a task.
        # It is a dictionary with the following keys:
        #   label:  Short, one line description of the task.
        #   task:   Method or function to run. If not set, or set to None,
        #           nothing is executed for that step.
        #   failed: This is the result of the task execution. The function
        #           defined by the "task" key must set that status to True or
        #           False. This status is used to display the completion
        #           status of the task.
        #   msgs:   List of error messages. Those messages may be set by the
        #           "task" function when the task fails. They are
        #           displayed to provide additional information to students.
        #           Each message in the list is a dictionary with the key
        #           set to "text" and the text message as a value.
        #           For example:
        #               { "text": "The system cannot be reached"}
        #
        # Remove these "How to use this template" comments
        #######################################################################
        """
        Prepare the system for starting the lab
        """
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            #####################
            # BEGIN example tasks
            {
                "label": "Task that succeeds",
                "task": self._start_sample_success_task,
            },
            steps.header("Subheader example, task below fails"),
            {
                "label": "Task that fails",
                "task": self._start_sample_failure_task,
            },
            steps.header("Another subheader example, rest of tasks succeed"),
            {
                "label": "Do nothing task that always succeeds",
                "failed": False,
            },
            {
                "label": "Do nothing task only runs 1/2 times",
                "failed": False,
                "condition": self._returns_true_or_false_at_50,
            },
            {
                "header": "Subheader example, task below fails",
            },
            {
                "label": "Do nothing task that always fails",
                "failed": True,
            },
            {
                "header": "Another subheader example, rest of tasks succeed",
            },
            # END example tasks
            #####################
            {
                "label": "PING host",
                "task": self._start_ping_host,
                "host": "localhost",
                "fatal": True,
            },
            {
                "label": "Check Red Hat release",
                "task": self._start_check_release,
            },
            {
                "label": "Check system services",
                "task": self._start_check_services,
            },
            {
                "label": "Copy exercise files",
                "task": labtools.copy_lab_files,
                "lab_name": self.__LAB__,
                "fatal": True,
            },
        ]
        userinterface.Console(items).run_items(action="Starting")

    def grade(self):
        #######################################################################
        #   How to use this template:
        #
        # Apart from the keys defined in the start function,
        # the grading function has a special key that is used when grading
        #
        #   grading:    Set to True to indicate that the task is part of
        #               the grading section for this lab script and the
        #               run_items function will print 'PASS' in blue if the
        #               task is successful.
        #
        #               If this key is either not present, not set, or set to
        #               False, then the run_items function will print 'SUCCESS'
        #               in green if the task is successful.
        #
        # Remove these "How to use this template" comments
        #######################################################################
        """
        Perform evaluation steps on the system
        """
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
                "grading": True,
            },
            #####################
            # BEGIN example tasks
            {
                "label": "Task that passes",
                "task": self._start_sample_success_task,
                "grading": True,
            },
            # Uncomment this to make the grading fail
            # {
            #     "label": "Task that fails",
            #     "task": self._start_sample_failure_task,
            #     "grading": True,
            # },
            # END example tasks
            #####################
            {
                "label": "Check sshd_config owner and permissions",
                "task": self._grade_check_sshd_config,
                "grading": True,
            },
            {
                "label": "Configuration file exists",
                "task": self._grade_check_conf,
                "lab_name": self.__LAB__,
                "grading": True,
            },
        ]
        ui = userinterface.Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()

    def finish(self):
        """
        Perform post-lab cleanup
        """
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
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

    def _start_sample_success_task(self, item):
        logging.debug(sys._getframe().f_code.co_name)
        item["failed"] = False
        time.sleep(1)

    def _returns_true_or_false_at_50(self):
        return random.choice([True, False])

    def _start_sample_failure_task(self, item):
        logging.debug(sys._getframe().f_code.co_name)
        item["failed"] = True
        item["msgs"] = [
            {"text": "Sample explanation of failure"},
            {"text": "Further explanation would go here"},
        ]
        time.sleep(1)

    def _start_ping_host(self, item):
        """
        Execute a task to prepare the system for the lab
        """
        logging.debug(sys._getframe().f_code.co_name)
        check = labtools.ping(item["host"])
        for key in check:
            item[key] = check[key]
        # Return status to abort lab execution when failed
        return item["failed"]

    def _start_check_release(self, item):
        """
        Check if workstation is running RHEL
        """
        logging.debug(sys._getframe().f_code.co_name)
        check = labtools.grep(
            "/etc/redhat-release",
            "Red Hat Enterprise Linux"
        )
        for key in check:
            item[key] = check[key]

        # Return status to abort lab execution when failed
        return item["failed"]

    def _start_check_services(self, item):
        """
        Check that system services are running
        """
        logging.debug(sys._getframe().f_code.co_name)
        # Note: This task can be performed with the systemd python
        # module but we need to compile it when installing via pip
        services = [
            "chronyd",
            "rsyslog",
            "sshd",
            "systemd-journald",
            "systemd-udevd",
            # Uncomment the following to make the task fail
            # "systemd-binfmt",
            # "systemd-timesyncd",
        ]
        for service in services:
            try:
                for check in ("is-enabled", "is-active"):
                    subprocess.run(
                        ["systemctl", check, service],
                        timeout=1,
                        check=True,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                item["failed"] = False
            except Exception as e:
                item["failed"] = True
                item["msgs"] = [
                    {
                        "text":
                            "Service is not " +
                            "'enabled' and 'active':" +
                            " {}".format(service)
                    }
                ]
                item["exception"] = {
                    "name": e.__class__.__name__,
                    "message": str(e),
                }
        # Return status to abort lab execution when failed
        return item["failed"]

    ###########################################################################
    # Grading tasks

    def _grade_check_sshd_config(self, item):
        """
        Check SSH configuration file
        """
        logging.debug(sys._getframe().f_code.co_name)
        path = "/etc/ssh/sshd_config"
        try:
            file_stat = os.stat(path)
            stat_info = stat.S_IMODE(file_stat.st_mode)

            # File must be owned by root:root
            if not (file_stat.st_uid == 0 and file_stat.st_gid == 0):
                raise LabError("File is not owned by 'root:root'")

            # File must be mode 0600
            if stat_info != (stat.S_IRUSR | stat.S_IWUSR):
                raise LabError("File does not have '0600' permissions")

            item["failed"] = False
        except LabError as e:
            item["failed"] = True
            item["msgs"] = [
                {
                    "text":
                        "File does not have desired owner and permissions: " +
                        "{}".format(path)
                }
            ]
            item["exception"] = {
                "name": e.__class__.__name__,
                "message": str(e),
            }

    def _grade_check_conf(self, item):
        """
        Test that the configuration file exists in student's working directory
        """
        logging.debug(sys._getframe().f_code.co_name)
        student_working_dir = os.path.join(
            labtools.get_sku_path(),
            "labs",
            item['lab_name'],
        )
        conf_file = os.path.join(student_working_dir, "test.conf")

        if not os.path.isfile(conf_file):
            item["failed"] = True
            item["msgs"] = [
                {
                    "text":
                        "Configuration file missing: {}".format(conf_file)
                }
            ]
        else:
            item["failed"] = False

    ###########################################################################
    # Finish tasks

    # (none)
