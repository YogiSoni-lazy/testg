"""
Common lab steps (DEPRECATED)
"""
from pathlib import Path
from typing import Union
import warnings
from labs.common import tasks
from labs import core
from labs.common import fs


def run_command(label, hosts, command, returns=0, options=None, prints='',
                fatal=False, student_msg='', sshkey='', shell=False,
                condition=None):
    warnings.warn(
        "This function is deprecated."
        "Use the labs.common.commands module instead",
        category=DeprecationWarning
    )
    if options is None:
        options = []
    if condition is None:
        def default_condition():
            return True
        condition = default_condition
    return {
                "label": label,
                "task": tasks.run_command,
                "hosts": hosts,
                "username": "root",
                "password": "redhat",
                "command": command,
                "returns": returns,
                "options": options,
                "prints": prints,
                "fatal": fatal,
                "student_msg": student_msg,
                "sshkey": sshkey,
                "shell": shell,
                "condition": condition,
    }


def header(header):
    warnings.warn(
        "This function is deprecated."
        "Use the labs.ui module instead",
        category=DeprecationWarning
    )
    return {
        "header": header
    }


def copy_lab_files(
    fromdir: Union[Path, str],
    to: Union[Path, str],
    no_source_error=True,
    label="Copying lab files to workspace",
    fatal=True
):
    """
    DEPRECATED

    Copies a directory into a destination.
    The `no_source_error` controls whether an error is raised if the source dir
    does not exist
    """
    warnings.warn(
        "This function is deprecated."
        "Use labs.common.fs.copy_materials_step instead",
        category=DeprecationWarning
    )
    return core.LabStep(
        label,
        task=tasks.copy_lab_files(fromdir, to, no_source_error),
        fatal=fatal
    )


def copy_materials_step(
    materials_path: Path,
    lab_name: str,
    to: Path,
    label="Copying lab files to workspace",
    fatal=True,
):
    warnings.warn(
        "This function is deprecated."
        "Use the labs.common.fs module instead",
        category=DeprecationWarning
    )
    return fs.copy_materials_step(materials_path, lab_name, to, label, fatal)
