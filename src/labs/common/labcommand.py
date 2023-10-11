#
# Copyright (c) 2021 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#

"""Run command script function library."""

import subprocess
import re
import logging
import os
from typing import Dict
import warnings

warnings.warn(
    "This module is deprecated. "
    "To run commands, "
    "use the labs.common.commands module",
    category=DeprecationWarning
)


def check_sshkey(item: Dict):
    """
    Checks if sshkey is in the Dict. If not, use standard location.

    :param item: dict containing:sshkey
    """
    if ("sshkey" in item) and (os.path.isfile(item["sshkey"])):
        sshkey = item["sshkey"]
    else:
        sshkey = '/home/student/.ssh/lab_rsa'

    return sshkey


def log_stdin(stdin: str):
    """
    Log stdin to info level in default log file.
    """

    if stdin:
        logging.info(f"\n\nSTDIN: \n\n{stdin}")


def log_stdout(stdout: str):
    """
    Log stdout to info level in default log file.
    """

    if stdout:
        logging.info(f"\n\nSTDOUT: \n\n{stdout}")


def log_stderr(stderr: str):
    """
    Log stderr to info level in default log file.
    """

    if stderr:
        logging.info(f"\n\nSTDERR: \n\n{stderr}")


def log_errormsg(error_list: list):
    """
    Log error_list in error level to the default log file
    """
    errors = []
    for p in error_list:
        for k, v in p.items():
            errors.append(v)
    ferror = "\n".join(errors)
    logging.error(f"\n\nERROR MESSAGES: \n\n{ferror}\n")


def student_message(message: str, log: str):
    """
    Append student message to the log string
    """
    if (message):
        log.append({"text": message})
    return 0


def run_log(*args, **kwargs):
    """
    Run any command logging stdout and stderr to the info level.
    This function makes use of the subprocess module.
    """

    cmd = f"Run command: {' '.join(*args)}\n"
    log_stdin(cmd)

    # Run the command through subprocess
    output = subprocess.run(*args, **kwargs)

    # Log to the configured stdout file
    log_stdout(output.stdout.decode("utf-8"))
    log_stderr(output.stderr.decode("utf-8"))

    return output


def check_prints(item, output):
    """
    Check if stdout prints target
    """
    prints: str = item.get("prints")
    student_msg: str = item["student_msg"]
    error_log = []
    ostr = str(output.stdout.decode("utf-8"))
    r = re.compile(prints, re.IGNORECASE)
    m = r.search(ostr)
    if not m:
        item["failed"] = True
        if "msgs" not in item:
            student_message(student_msg, error_log)
        msg = "Command did not print the expected message"
        error_log.append({"text": msg})
        msg = f"'{prints}' not found in command output"
        error_log.append({"text": msg})
        if "msgs" in item:
            item["msgs"] = item["msgs"] + error_log
        else:
            item["msgs"] = error_log


def check_retcode(item, output):
    """
    Check if return code is correct
    """
    returns: int = item.get("returns")
    student_msg: str = item["student_msg"]
    error_log = []
    if int(returns) != output.returncode:
        item["failed"] = True
        if "msgs" not in item:
            student_message(student_msg, error_log)
        msg = "Command did not exit with the expected code"
        error_log.append({"text": msg})
        msg = f"Expected: {returns}, Received: {output.returncode}"
        error_log.append({"text": msg})
        if "msgs" in item:
            item["msgs"] = item["msgs"] + error_log
        else:
            item["msgs"] = error_log
