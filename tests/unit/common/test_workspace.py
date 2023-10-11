
import os
from pathlib import Path
import tempfile
import pytest
from tests._util.workspace import DummyConfig, create_tmp_configfile
from unittest.mock import MagicMock
from labs.common.workspace import Workspace


class TestWorkspace:

    """
    Tests workspace configuration functionality
    """
    workdir: str
    configfile_path: str
    workspace: Workspace

    def setup_method(self):
        self.configfile_path = create_tmp_configfile()
        self.workdir_path = tempfile.mkdtemp()
        self.workspace = Workspace()

    def test_configure_saves_workspace_path(self):
        # Given some config
        config = DummyConfig(self.configfile_path, self.workdir_path)

        # When workspace is configured
        self.workspace.configure(config)

        # Then the workdir config is set
        assert self.workspace.config.workdir == self.workdir_path

    def test_configure_saves_config_in_configfile(self):
        # Given a config with the path for the workspace
        config = MagicMock()
        config.workdir = self.workdir_path

        # When workspace is configured
        self.workspace.configure(config)

        # Then the config is saved in the config file
        config.save.assert_called()

    def test_is_current_dir(self):
        # Given current working dir
        config = DummyConfig(self.configfile_path, os.getcwd())

        # When workspace is configured to be the cwd
        self.workspace.configure(config)

        # Then
        assert self.workspace.is_current_directory() is True

    def test_copy_dir(self):
        # Given a configured workspace
        config = DummyConfig(self.configfile_path, self.workdir_path)
        self.workspace.configure(config)
        # Given a folder to copy into the workspace
        os.makedirs(Path(self.workdir_path, "SKU-apps/my-test-lab", "apps"))

        # When copying a workspace/source to workspace/destination
        self.workspace.copy_subdir("SKU-apps/my-test-lab/apps", "my-test-lab")

        # Then the new copied dir exists
        expected = Path(self.workdir_path, "my-test-lab")
        assert expected.exists()

    def test__copy_dir__source__doesnt__exist(self):
        """
        When copying dirs, if the source doesn't exist,
        the destination is not created
        """
        # Given a configured workspace
        config = DummyConfig(self.configfile_path, self.workdir_path)
        self.workspace.configure(config)

        # When copying a workspace/source to workspace/destination
        self.workspace.copy_subdir(
            "does/not/exist",
            "my-test-lab")

        # Then the new copied dir does not exist
        expected = Path(self.workdir_path, "my-test-lab")
        assert not expected.exists()

    def test__copy_dir__source__doesnt__exist__failure(self):
        """
        When copying dirs,
            if the source doesn't exist,
            and
            the "fail_if_no_source" is True
        an Exception is raised
        """
        # Given a configured workspace
        config = DummyConfig(self.configfile_path, self.workdir_path)
        self.workspace.configure(config)

        # When copying a workspace/source to workspace/destination
        # an OSError should be raised
        with pytest.raises(OSError) as error_info:
            self.workspace.copy_subdir(
                "does/not/exist",
                "my-test-lab",
                no_source_error=True
            )

        assert "not a directory or does not exist" in str(error_info.value)
