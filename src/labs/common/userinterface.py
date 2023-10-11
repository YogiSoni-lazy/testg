#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#

"""Display progress and status of the lab module executions."""

import logging
from typing import Callable, List, Optional, Union, Dict

from halo import Halo
from click import echo, secho, style

from labs import labconfig
from labs.core.step import LabStep, ensure_labsteps
from labs.core.task.runner import run_task
from labs.watch import watch
from labs.watch.watchstep import LabWatchStep
from labs.laberrors import LabError


class Console:
    """Format messages.

    :param bullet: Bullet point for additional messages. " - " by default.
    :type bullet: str
    :param status_length: Max lenght of the status string. Those strings are
                          the one that are added at the end of the lines (FAIL,
                          SUCCESS, ...) Default: 10
    :type status_length: int
    :param spinner_delay: Seconds to wait for the execution of each task.
                          1 second by default
    :type  spinner_delay: int
    """

    def __init__(
        self,
        items: List[Union[Dict, LabStep]],
        watch_items: Optional[List[LabWatchStep]] = None,
        bullet=" - ",
        status_length=7,
        spinner_delay=None,
    ):
        """Initialize the object."""
        self.bullet = bullet
        self.status_length = status_length
        self.spinner_delay = spinner_delay
        self.items = ensure_labsteps(items)
        self.watch_items = watch_items or []

    def run_items(self, action="Starting"):
        """
        Process each item in the given list.
        Each item in the list is a dictionary. The function uses the following
        keys:

        "task": Function to execute. If None or not set, nothing is executed.
                That function is called with the item dictionary as parameter.
                If the function returns True (the truth), then the execution
                stops immediately and the other following task in the list are
                not run.
        "failed": The function defined in "task" can set this key. If False,
                then the success status is reported. If True, then a failed
                status is reported to students. In addition, if the "msgs" key
                is also set, those messages are also displayed to provide more
                details on the failure.
        "msgs": List of additional error messages when the task failed. Each
                element of that list is a dictionary with the key set to
                "text" and the message as the value.
        "grading": Boolean flag to indicate if the executed item is for grading
                purposes. If defined and True, then a 'PASS' string is echoed
                in blue. In other cases, a 'SUCCESS' string is echoed in green.

        :param action: The lab action that the function is peforming.
                       This action is printed to stdout
        :type action: str
        """
        secho("\n%s lab.\n" % action, bold=True)
        for item in self.items:
            if not item.condition():
                logging.debug(f"{item} was skipped due to false condition")
                continue

            if item.is_header():
                echo_header(item)
                continue

            with Halo(
                text=item.label,
                spinner=get_spinner(),
                interval=self.spinner_delay or -1,
                enabled=not labconfig.is_dev_mode(),
            ) as spinner:

                if item.has_task():
                    ret_code = run_task(item)
                else:
                    ret_code = 0

                # TODO: fix ret_code condition
                # What is a failure?
                #
                #   integer, greater-than-zero ret_codes?
                #
                # Right now the condition fails if the ret_code is truthy,
                # which means non-empty lists/strings, True... or any
                # other expression that evaluates to True is considered a FAIL
                failed = item.failed or ret_code

                self.echo_item_result(item, failed, spinner)

                self.echo_secondary_messages(item)

                if failed and item.fatal:
                    self.echo_fatal(action)
                    msg = f"The '{item.label}' fatal step has failed"
                    logging.error(msg)
                    raise LabError(msg)
        echo("")

        return self

    def report_grade(self):
        status = style("PASS", fg='green')

        for item in self.items:
            if item.failed:
                status = style("FAIL", fg='red')
                break

        echo(f"Overall lab grade: {status}\n")

    def watch_lab(
        self,
        action="Tracking lab progress...",
        sleep_seconds=1,
        finish: Callable = None
    ):
        """
        Watches lab progress by continously
        executing the list of watch steps provided in the
        "watch_items" property of the class constructor.

        :param action: The lab action that the function is peforming.
                       This action is printed to stdout
        :type action: str

        :param sleep_seconds: Number of seconds to wait between watch rounds.
                              One second by default
        :type sleep_seconds: int

        :param on_finish: lab finish function to invoke
                          after all the checkpoints pass
        :type on_finish: Callable
        """
        watch(
            self.watch_items,
            action,
            sleep_seconds,
            finish
        )

    def echo_header(self, item):
        echo()
        echo(item["header"])
        echo()

    def echo_item_result(self, item: LabStep, failed: bool, spinner):
        emphasized_label = style(item.label, bold=True)

        if failed:
            spinner.stop_and_persist(
                symbol=style(self.status("FAIL"), fg="red"),
                text=emphasized_label
            )
        else:
            if item.grading:
                spinner.stop_and_persist(
                    symbol=style(self.status("PASS"), fg='blue'),
                    text=emphasized_label
                )
            else:
                spinner.stop_and_persist(
                    symbol=style(self.status("SUCCESS"), fg="green"),
                    text=emphasized_label
                )

    def echo_secondary_messages(self, item):
        for text in item.get_text_messages():
            echo(self.get_secondary_message(text))

    def get_secondary_message(self, message):
        """Return the formated message for second level.
        :param message: Message to format
        :type message: str
        :returns: The formated message (with a bullet in front)
        """
        return " " * self.status_length + self.bullet + message

    def echo_fatal(self, action):
        echo(style(
            self.get_secondary_message(
                f"Cannot continue {action.lower()} lab",
            ),
            fg="red"
        ))

    def status(self, msg):
        return msg.ljust(self.status_length)


def echo_header(item):
    echo()
    echo(item["header"])
    echo()


def get_spinner():
    return {
        "interval": 130,
        "frames": [
            "   -   ",
            "   \\   ",
            "   |   ",
            "   /   "
        ]
    }
