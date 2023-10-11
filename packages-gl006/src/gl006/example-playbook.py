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

import sys
import logging

from labs import labconfig
from labs.grading import Default
from labs.common import labtools, userinterface

# List your Ansible Playbooks.
# The path is relative to the gl006 directory.
# If you do not support a subcommand (start, grade, finish), remove the
# corresponding start(), grade(), finish() methods
_playbook_start = "ansible/examplePlaybook/playbookStart.yml"
_playbook_grade = "ansible/examplePlaybook/playbookGrade.yml"
_playbook_finish = "ansible/examplePlaybook/playbookFinish.yml"

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
class ExamplePlaybook(Default):
    """
    Example Playbook lab script for GL006
    """
    __LAB__ = 'example-playbook'

    def _example_failure(self, item):
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
        item["failed"] = True
        item["msgs"] = [{"text": "Task failed on purpose for an example"}]

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.
    #
    # If you only use playbooks, you do not have to modify anything in those
    # methods.

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
            {
                "label": "Running Ansible Playbook",
                "task": self.run_playbook,
                "playbook": _playbook_start,
                "vars": {
                    "abc": "999"
                },
            },
        ]
        userinterface.Console(items).run_items()

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
            },
            {
                "label": "Running Ansible Playbook",
                "task": self.run_playbook,
                "playbook": _playbook_grade,
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
                "task": self._example_failure,
                "hosts": _targets,
                "fatal": True,
            },
            {
                "label": "Running Ansible Playbook",
                "task": self.run_playbook,
                "playbook": _playbook_finish,
            },
        ]
        userinterface.Console(items).run_items(action="Finishing")
