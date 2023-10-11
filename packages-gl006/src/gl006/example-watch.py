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

import random

from labs.grading import Default
from labs.watch import watchstep, expect
from labs.common.userinterface import Console


# Change the class name to match your file name with WordCaps
class ExamplePythonWatch(Default):
    """
    Example Python lab WATCH script for GL006
    """
    __LAB__ = "example-watch"

    # The following methods define which subcommands are supported
    # (start, grade, finish). Remove the methods you do not need.

    def start(self):

        """
        Prepare the system for starting the lab
        """
        items = [
            {
                "header": "Subheader example, task below fails",
            },
            {
                "label": "Do nothing task that always fails",
                "failed": True,
            }
        ]

        # -- Example of lab watch --
        #
        # The "watch" function watches the lab progress by continously
        # executing a list of checks, called watchsteps.
        #
        # The lab script finishes when all checks pass.
        # Check funcions must be decorated with "@watchstep"

        watch_items = [
            my_watch_step,
            my_watch_step,
            my_watch_step,
            raise_exception
        ]

        console = Console(
            items,
            watch_items
        )

        console.run_items(action="Starting").watch_lab(finish=self.finish)


# Lab Watch Steps


# -- A "Lab Watch Step" is a check used by lab watch --
#
# A watch step funcion requires:
# - The @watchstep decorator, to set the description of the watch step
# - The use of "expect" to validate a condition
# - (Optional) An error message, shown if the check does not pass
# - (Optional) A list of hint messages, shown if the check does not pass
@watchstep("This is another check of the lab progress")
def my_watch_step():

    # Use expect to validate a condition
    expect(
        random.randint(0, 10) > 5,
        error="This failure was intended",
        hints=["This step fails randomly. Wait for subsequent check rounds"]
    )


@watchstep("This step raises an exception")
def raise_exception():

    def check():
        raise KeyError("key does not exist")

    expect(
        check(),
        error="This failure was intended",
        hints=["This step fails randomly. Wait for subsequent check rounds"]
    )
