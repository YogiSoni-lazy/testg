"""
File system utilities
"""

import os
import logging
import shutil
from pathlib import Path
from labs.ui.step import Step


_DIR_TYPES = ["labs", "solutions"]


def copy_materials_step(
    materials_path: Path,
    lab_name: str,
    to: Path,
    label="Copying lab files to workspace",
    fatal=True,
):
    """
    UI Step to copy the content of the lab materials to the student lab path.

    :param materials_path: Path of the materials folder
    :param lab_name: name of the lab
    :param to: destination where the labs/lab_name and
        solutions/lab_name materials will be copied
    :param label: Optional label to override the default
    :param fatal: stop if the step fails
    """
    with Step(message=label, fatal=fatal) as step:
        if not materials_path.is_dir():
            raise OSError(f"{materials_path} is not a "
                          f"directory or does not exist")
        else:
            for dir_type in _DIR_TYPES:
                src_path = materials_path / dir_type / lab_name
                dst_path = to / dir_type / lab_name
                if not _overwrite_enabled() and _path_has_content(dst_path):
                    step.add_message(
                        f"Path {dst_path} not empty... "
                        + "Execute OVERWRITE=true lab start ... to "
                        + "overwrite the files"
                    )
                    continue
                if not src_path.is_dir():
                    logging.warning(
                        f"Lab '{lab_name}' does not have a"
                        f" '{dir_type}' directory"
                    )
                    continue
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src=src_path, dst=dst_path)

        return step


def _overwrite_enabled():
    return os.getenv("OVERWRITE", "").lower() in ["yes", "1", "true"]


def _path_has_content(path: Path):
    return path.exists() and bool(os.listdir(path))
