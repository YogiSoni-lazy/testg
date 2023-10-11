"""
Utils to create temporary workspaces in test scenarios
"""

import os
import tempfile
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory
from labs.common.config import ClassroomConfigFile
from labs.common.workspace import Workspace


class DummyConfig(ClassroomConfigFile):

    """ Dummy config class for tests"""

    def load(self):
        pass

    def save(self, output: bool = True):
        pass


def create_tmp_configfile():
    return os.path.join(
        tempfile.mkdtemp(),
        "workspace_test.json"
    )


@contextmanager
def test_workspace():
    """
    Creates a temp workdir for the workspace
    """
    with NamedTemporaryFile() as configfile:
        with TemporaryDirectory() as tmpdir:
            workdir = os.path.join(tmpdir, "rht-labs-core-test")
            config = DummyConfig(configfile.name, workdir)
            w = Workspace().configure(config)
            yield w
