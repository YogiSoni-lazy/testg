
"""
Library module for running commands.

A wrapper over the `subprocess` module to
execute commands and verify the result.
"""

import logging
import subprocess
from typing import List, Optional, Tuple

from labs.ui import Step


def run_command_step(
    message: str,
    command: str,
    options: List[str] = [],
    shell=False,
    prints: Optional[str] = None,
    returns: Optional[int] = None,
    grading=False,
    fatal=False
) -> Tuple[subprocess.CompletedProcess, Step]:
    """A UI Step to run a command.

    Step to run a command on localhost.
    This step wraps the `run_command` function.

    Args:
        message: the Step message
        command: A string with the command to be run.
            If `shell=True`,
            this string can be used to add options or pipes.
        options: List of additional command options
        shell: set to True to pass the entire command as a single string
        prints: look for a specific string in
            the stdout (case-insensitive)
        returns: look for a specific return code
            at the output of the command
        grading: Flag to use a grading step
        fatal: Flag to use a fatal step

    Returns:
        The step
    """

    with Step(message, grading=grading, fatal=fatal) as step:
        process = run_command(command, options, shell)

        verify_command_result(step, process, prints, returns)

    return process, step


def verify_command_succeeds(
    step: Step,
    process: subprocess.CompletedProcess,
):
    """
    Alias of `verify_command_result` to check that a command has
    returned a 0 error code
    """
    return verify_command_result(step, process, returns=0)


def verify_command_result(
    step: Step,
    process: subprocess.CompletedProcess,
    prints: Optional[str] = None,
    returns: Optional[int] = None
):
    """
    Mark a step as failed (adding error messages)
    if the command result is not the expected

    Args:
        step: the Step
        process: the completed process
        prints: look for a specific string in
            the stdout (case-insensitive)
        returns: look for a specific return code
            at the output of the command
    Returns:
        True if the verification is successful, False otherwise
    """
    if prints is not None:
        expected_stdout = prints.lower()
        actual_stdout = process.stdout.decode().lower()

        if expected_stdout not in actual_stdout:
            step.add_errors([
                f"'{process.args}' did not print the expected message",
                f"'{prints}' not found in command output"
            ])

            return False

    if returns is not None and returns != process.returncode:
        step.add_errors([
            f"'{process.args}' did not exit with the expected code",
            f"Expected: {returns}, Received: {process.returncode}"
        ])

        return False

    return True


def run_command(
    command: str,
    options: List[str] = [],
    shell=False
):
    """
    Run a command on localhost.
    Returns a CompletedProcess object.

    Args:
        command: A string with the command to be run.
            If `shell=True`,
            this string can be used to add options or pipes.
        options: List of additional command options
        shell: set to True to pass the entire command as a single string

    Returns:
        The completed process
    """

    full_command = [command] + options

    process = _run_command_and_log(full_command, shell)

    return process


def _run_command_and_log(command: List[str], shell=False):
    command_str = " ".join(command)
    logging.info(f"\n\nCOMMAND: \n\n{command_str}")

    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell
    )

    # Log to the configured stdout file
    stdout = process.stdout.decode()
    logging.info(f"\n\nSTDOUT: \n\n{stdout}")

    stderr = process.stderr.decode()
    logging.error(f"\n\nSTDERR: \n\n{stderr}")

    return process
