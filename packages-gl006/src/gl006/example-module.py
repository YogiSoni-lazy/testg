#
# Copyright (c) 2021 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#
# CHANGELOG
# * Sep 28 2021 Your Name <yname@redhat.com>
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


from labs.grading import Default
from labs import labconfig
from labs.common import userinterface

# Import all the functions defined in the common.py module
from gl006 import common


# Course SKU
SKU = labconfig.get_course_sku().upper()

# List of hosts involved in that module. Before doing anything,
# the module checks that they can be reached on the network
_targets = [
    "localhost",
]


# Change the class name to match your file name with WordCaps
class ExampleModule(Default):
    """
    This is the DocString for the ExampleModule class
    """
    __LAB__ = "example-module"

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.

    def start(self):
        """
        Prepare the system for starting the lab
        """
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
        items = [
            {
                # This task is defined in the common.py file
                "label": "Call a function from a module",
                "task": common.common_task,
                "message": "sample message called from the start function",
                "fatal": True,
            },
        ]
        userinterface.Console(items).run_items(action="Starting")

    def grade(self):
        """
        Perform evaluation steps on the system
        """
        logging.debug("{} / {}".format(SKU, sys._getframe().f_code.co_name))
        items = [
            {
                # This task is defined in the common.py file
                "label": "Call a function from a module",
                "task": common.common_task,
                "message": "sample message called from the grade function",
                "fatal": True,
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
                # This task is defined in the common.py file
                "label": "Call a function from a module",
                "task": common.common_task,
                "message": "sample message called from the finish function",
                "fatal": True,
            },

        ]
        userinterface.Console(items).run_items(action="Finishing")
