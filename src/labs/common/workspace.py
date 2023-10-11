import os
import warnings
from pathlib import Path
from typing import Generic, Optional, TypeVar, Union
from labs.common.config import ClassroomConfigFile
from labs.common.labtools import copy_or_replace_dir
from labs.common.userinterface import echo


# To make type hints work with subclasses
C = TypeVar("C", bound=ClassroomConfigFile)


class Workspace(Generic[C]):

    """DEPRECATED: Use `labs.common.config.parse_config` instead

    A "Workspace" instance is an abstraction of the config and
    the working directory that the student will use to
    perform the labs in a course

    This class configures the classroom env variables,
    creates a working directory
    and exposes utility workspace functions
    """

    config: C

    def __init__(self, config: Optional[C] = None):
        """
        Args:
            config: A subtype of :obj:`labs.common.config.ClassroomConfigFile`
        """
        warnings.warn(
            "This class is deprecated. "
            "Use labs.common.config.parse_config() instead",
            category=DeprecationWarning
        )

        if config:
            self.config = config
            self.config.load()

    def configure(self, config: C, output: bool = True):
        """
        Creates the workspace directory and configuration file

        Args:
            config: A subtype of :obj:`labs.common.config.ClassroomConfigFile`
            output: Whether or not to produce an output message
                    after the workspace has been configured
        """
        self.config = config
        self.config.save(output)
        self.create_workdir(output)
        return self

    def create_workdir(self, output: bool = True):
        """
        Creates the workspace directory if it does not exist
        """
        try:
            os.mkdir(self.config.workdir)
            if output:
                echo(f"Directory {self.config.workdir} created")
        except FileExistsError:
            if output:
                echo(f"Directory {self.config.workdir} already exists")

    def exists(self):
        """
        Checks if the workspace directory exists
        """
        workdir = self.config.workdir
        return workdir and os.path.isdir(workdir)

    def is_current_directory(self):
        """
        Checks if the current working directory is the workspace
        """
        cwd = os.path.abspath(os.getcwd())
        return os.path.abspath(self.config.workdir) == cwd

    def path(self, dir: str):
        """
        Returns the absolute path of a specific directory within the workspace
        """
        workdir = self.config.workdir or ""
        return os.path.join(workdir, dir)

    def copy_subdir(
        self,
        relative_source: Union[Path, str],
        relative_destination: Union[Path, str],
        no_source_error=False,
    ):
        """
        Copy directories inside the workspace
        Directory paths are relative to the workspace path

        If "no_source_error" is True, raise an exception
        if the source does is not a directory
        """

        source = self.path(relative_source)
        destination = self.path(relative_destination)

        copy_or_replace_dir(source, destination, no_source_error)
