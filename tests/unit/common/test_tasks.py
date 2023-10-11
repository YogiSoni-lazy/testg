"""
labs.common.tasks tests
"""
import os
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch
import pytest
from labs import common
from labs.core.task import task, TaskException, TaskFailure, TaskSuccess
from labs.common.git.repository import GitRepoError
from tests._util.workspace import test_workspace


class TestMkdir(TestCase):

    """
    mkdir()
    """

    def test_succeeds(self):
        """
        Succeeds when folder is created sucessfully in the workspace
        """
        with test_workspace() as workspace:

            item = {
                "path": workspace.path("my-test-folder")
            }
            common.tasks.mkdir(item)

            assert item["failed"] is False


class TestRmDir(TestCase):

    """
    remove_folder_from_workspace()
    """

    def test_succeeds_if_folder_doesnt_exist(self):
        """
        Succeeds if the folder does not exist
        """
        with test_workspace() as workspace:
            item = {
                "path": workspace.path("my-test-folder")
            }
            common.tasks.rmdir(item)

            assert item["failed"] is False

    def test_succeeds_if_folder_exists(self):
        """
        Succeeds if the folder exists and is removed
        """
        with test_workspace() as workspace:
            # Given that the folder exists in the workspace
            os.mkdir(os.path.join(workspace.config.workdir, "my-folder"))

            item = {
                "path": workspace.path("my-folder")
            }
            common.tasks.rmdir(item)

            assert item["failed"] is False


class TestCheckGitConfig(TestCase):

    """
    check_git_config()
    """

    @patch("labs.common.tasks.gitconfig")
    def test_fails_if_user_not_set(self, gitconfig):

        gitconfig.username.return_value = None

        item = {}
        common.tasks.check_git_config(item)

        assert item["failed"] is True

    @patch("labs.common.tasks.gitconfig")
    def test_fails_if_email_not_set(self, gitconfig):

        gitconfig.email.return_value = None

        item = {}
        common.tasks.check_git_config(item)

        assert item["failed"] is True

    @patch("labs.common.tasks.gitconfig")
    def test_succeeds_if_email_and_user_set(self, gitconfig):

        gitconfig.email.return_value = "example@example.com"
        gitconfig.username.return_value = "My Name"

        item = {}
        common.tasks.check_git_config(item)

        assert item["failed"] is False


class TestCheckGitRemotePointsTo(TestCase):

    """
    check_git_remote_points_to()
    """

    @patch("labs.common.tasks.repository")
    def test_succeeds(self, repository):
        """
        Succeeds when remote URL ends with the given remote repo name
        the followed by ".git" suffix
        """
        repository.get_remote_urls.return_value = [
            "git@github.com:user/remote-reponame.git"
        ]

        with test_workspace() as workspace:
            item = {
                "repopath": workspace.path("repo/dir"),
                "remote_repo_name": "remote-reponame"
            }
            common.tasks.check_git_remote_points_to(item)

        assert item["failed"] is False

    @patch("labs.common.tasks.repository")
    def test_fails(self, repository):
        """
        Fails when remote URL does not include the repo name
        """
        repository.get_remote_urls.return_value = []

        with test_workspace() as workspace:
            item = {
                "repopath": workspace.path("repo/dir"),
                "remote_repo_name": "remote-reponame"
            }
            common.tasks.check_git_remote_points_to(item)

        assert item["failed"] is True

    @patch("labs.common.tasks.repository")
    def test_uses_repo_relative_to_workspace(self, repository):
        """
        Uses a local repository path relative to the workspace dir
        """
        with test_workspace() as workspace:
            item = {
                "repopath": workspace.path("repo/dir"),
                "remote_repo_name": "remote-reponame"
            }
            common.tasks.check_git_remote_points_to(item)

            repository.get_remote_urls.assert_called_with(
                f"{workspace.config.workdir}/repo/dir",
                "origin")


class TestCheckGitLocalRepositoryExists(TestCase):

    """
    check_git_local_repo_exists()
    """

    @patch("labs.common.tasks.repository")
    def test_succeeds(self, repository):
        """
        Succeeds when local repo exists
        """
        repository.exists.return_value = True

        with test_workspace() as workspace:
            item = {
                "repopath": workspace.path("repo/dir")
            }
            common.tasks.check_git_local_repo_exists(item)

        assert item["failed"] is False

    @patch("labs.common.tasks.repository")
    def test_fails(self, repository):
        """
        Fails when local DOES NOT exists
        """
        repository.exists.return_value = False

        with test_workspace() as workspace:
            item = {
                "repopath": workspace.path("repo/dir")
            }
            common.tasks.check_git_local_repo_exists(item)

        assert item["failed"] is True


class TestCheckFileIncludes(TestCase):

    """
    grep()
    """

    def test_succeeds(self):
        """
        Succeeds when the given content is present in a file
        """
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"some expected text")
            tmpfile.flush()

            item = {
                "filepath": tmpfile.name,
                "content": "expected text"
            }
            common.tasks.grep(item)

            assert item["failed"] is False

    def test_fails(self):
        """
        Fails when the given content is NOT present in a file
        """
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"some expected text")
            tmpfile.flush()

            item = {
                "filepath": tmpfile.name,
                "content": "expected TEXT"
            }
            common.tasks.grep(item)

            assert item["failed"] is True

    def test_fails_if_file_does_not_exist(self):
        """
        Fails when the file does not exist
        """
        item = {
            "filepath": "some/path/to.fail",
            "content": "expected text"
        }
        common.tasks.grep(item)

        assert item["failed"] is True

    def test_ignore_case(self):
        """
        Succeeds with case insensitive matching
        """
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"some expected text")
            tmpfile.flush()

            item = {
                "filepath": tmpfile.name,
                "content": "expected TEXT",
                "ignorecase": True
            }

            common.tasks.grep(item)

            assert item["failed"] is False


class TestGitCheckout(TestCase):

    """
    git_checkout()
    """

    @patch("labs.common.tasks.repository")
    def test_succeeds(self, repository):
        """
        Succeeds when git checkout does not raise exception
        """

        with test_workspace() as workspace:
            item = {
                "command": ["checkout", "main"],
                "repopath": workspace.path("repo/dir"),
            }
            common.tasks.git(item)

        assert item["failed"] is False

    @patch("labs.common.tasks.repository.run")
    def test_fails(self, run):
        """
        Fails when git checkout raises exception
        """
        run.side_effect = GitRepoError("test error")

        with test_workspace() as workspace:
            item = {
                "command": ["checkout", "main"],
                "repopath": workspace.path("repo/dir"),
            }
            common.tasks.git(item)

        assert item["failed"] is True


class TestTaskDecorator(TestCase):

    """
    @task decorator
    """

    def test__return__none__succeeds(self):
        """
        A funcion decorated with @task
        is considered sucessful if the function
        does not return anything
        """

        @task
        def dummy():
            pass

        taskfn = dummy()
        item = {}
        taskfn(item)

        assert "failed" not in item

    def test__throw_raise_taskexception__causes_fatal(self):
        """
        A funcion decorated with @task
        fails if the function
        raises a TaskException
        """

        @task
        def dummy():
            raise TaskException("error")

        taskfn = dummy()
        item = {}
        taskfn(item)

        assert item["failed"] is True

    def test__returning_tasksuccess(self):
        """
        A funcion decorated with @task
        is succeeds if the function returns
        TaskSuccess
        """

        @task
        def dummy():
            return TaskSuccess()

        taskfn = dummy()
        item = {}
        taskfn(item)

        assert "failed" not in item

    def test__returning_taskfailure(self):
        """
        A funcion decorated with @task
        fails if the function returns
        TaskFailure
        """

        @task
        def dummy():
            return TaskFailure()

        taskfn = dummy()
        item = {}
        taskfn(item)

        assert item["failed"] is True


class TestCheckCommandResult(TestCase):

    """
    check_command_result()
    """

    # Inject the "fp" fixture into the class
    @pytest.fixture(autouse=True)
    def _prepare_fixture(self, fp):
        self.fp = fp

    def test_verifies_return_code_0(self):
        """
        Expect a command to exit with exit code 0
        """
        # Use the fake process(fp) plugin
        # to define the expected subprocess calls
        self.fp.register(["ls"], returncode=0)

        item = {
            "command": "ls",
            "returns": 0
        }

        common.tasks.check_command_result(item)

        assert not item["failed"]

    def test_verifies_return_code_1(self):
        """
        Expect a command to exit with exit code 0
        but the command exits with non-zero code
        """
        # Use the fake process(fp) plugin
        # to define the expected subprocess calls
        self.fp.register(["ls"], returncode=1)

        item = {
            "command": "ls",
            "returns": 0
        }

        common.tasks.check_command_result(item)

        assert item["failed"]
