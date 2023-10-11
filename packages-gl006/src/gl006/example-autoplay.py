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
# 3. Rename the class using WordCaps
# 4. Set the __LAB__ variable to match the file name
#    (without the .py extension)
# 5. Remove these "How to use this template" comments
###############################################################################

from labs.grading import AutoPlay


# Change the class name to match your file name with WordCaps
class ExampleAutoPlay(AutoPlay):
    """
    Example Autoplay lab script for GL006
    """
    __LAB__ = 'example-autoplay'
