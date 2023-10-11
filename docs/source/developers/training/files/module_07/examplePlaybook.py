#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#
# CHANGELOG
#   * Mon Oct 05 2020 Your Name <yname@redhat.com>
#   - original code

"""Grading module for RH000 LAB_OR_GE_TITLE guided exercise (or lab).

This module either does start, grading, or finish for the
LAB_OR_GE_TITLE guided exercise (or lab).
"""

#########################################################################
#########################################################################
#                   How to use this template:
#
# 1. Rename the file to somethingRelatedToYourLab.py. Use camel case, do not
#    use dashes or underscores.
# 2. Adjust the CHANGELOG and docstring above.
# 3. Define your playbook files in the _playbook_start, _playbook_grade, and
#    _playbook_finish variables below.
# 4. Define the hosts that are used in this activity in the _targets variable.
# 5. Rename the class. The name of the class must match the file name (without
#    the .py extension)
# 6. Remove the methods (start, finish, or grade) that your lab script does
#    not support.
# 7. Remove these "How to use this template" comments
#########################################################################
#########################################################################

from labs.grading import Default
from labs.common import labtools, userinterface

# List your Ansible Playbooks.
# The path is relative to the gl006 directory.
# If you do not support a subcommand (start, grade, finish), remove the
# corresponding start(), grade(), finish() methods
_playbook_start = "ansible/examplePlaybook/playbookStart.yml"
_playbook_grade = "ansible/examplePlaybook/playbookGrade.yml"
_playbook_finish = "ansible/examplePlaybook/playbookFinish.yml"

# List of hosts involved in that module. Before doing anything,
# the module checks that they can be reached on the network
_targets = ["localhost"]
# _targets = ["servera", "serverb"]


# Change the class name to match your file name.
class ExamplePlaybook(Default):
    """Activity class."""
    __LAB__ = 'example-playbook'

    def _example_failure(self, item):
        item["failed"] = True
        item["msgs"] = [{"text": "Task failed on purpose for an example"}]
    #
    # The following methods define which subcommands are supported (start,
    # grade, finish).
    # Remove the methods you do not need.
    #
    # If you only use playbooks, you do not have to modify anything in those
    # methods.
    #

    def start(self):
        """Prepare the system for starting the lab."""
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True
            },
            {
                "label": "Running Ansible Playbook",
                "task": self.run_playbook,
                "playbook": _playbook_start,
                "vars": {"abc": "999"}
            },
        ]
        userinterface.Console(items).run_items()

    def grade(self):
        """Perform evaluation steps on the system."""
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True
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
        """Perform post-lab cleanup."""
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True
            },
            {
                "label": "Running Ansible Playbook",
                "task": self.run_playbook,
                "playbook": _playbook_finish,
            },
        ]
        userinterface.Console(items).run_items(action="Finishing")
