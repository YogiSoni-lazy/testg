"""
labs.common.git tests


These tests need a local repository to pass.
"""

from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from git.exc import GitCommandError
import pytest

from labs.common.git import repository


class TestExists(TestCase):

    """
    exists()
    """

    def test_repository_exists(self):
        """
        Returns True if a git repo exists in the given dir
        """
        repodir = get_repo_root_dir()
        assert repository.exists(repodir)

    def test_repository_exists_fail_if_no_repo_exists(self):
        """
        Returns False if no git repo exists in the given dir
        """
        with TemporaryDirectory() as repodir:
            assert repository.exists(repodir) is False

    def test_fails_if_folder_not_found(self):
        """
        Returns False if the dir does not exist
        """
        assert repository.exists("/some/missing/folderrrr") is False


class TestClone():

    """
    clone()
    """

    @patch('labs.common.git.repository.Repo')
    def test_calls__repo_clone_from(self, repoclass):

        repository.clone("https://remote/repo", "/local/path")

        repoclass.clone_from.assert_called_with(
            "https://remote/repo",
            "/local/path"
        )


class TestGetRemote():

    """
    has_remote()
    """

    def test_returns_the_remote_url(self):
        """
        Returns the remote URLs
        """
        repodir = get_repo_root_dir()
        urls = repository.get_remote_urls(repodir, "origin")
        for url in urls:
            assert url.endswith(".git")

    def test_returns_empty_list(self):
        """
        Returns empty list if the remote does not exist
        """
        repodir = get_repo_root_dir()
        urls = repository.get_remote_urls(repodir, "invalid-remote-name")
        assert urls == []


class TestGetBranches():

    """
    get_branches()
    """

    def test_returns_true_when_remote_exists(self):
        """
        Returns the list of branches (at least a main or master branch)
        """
        repodir = get_repo_root_dir()
        branches = repository.get_branches(repodir)
        assert type(branches) is list


class TestGetLatestCommits():

    """
    get_latest_commits()
    """

    def test_returns_list_of_commit_hashes_for_a_branch(self):
        """
        Returns the list of commit hashes
        """
        repodir = get_repo_root_dir()
        hashes = repository.get_latest_commits(repodir)
        assert len(hashes) > 0

    @patch('labs.common.git.repository.Repo')
    def test_raises_exception(self, repoclass):
        # When the PyGit lib raises a GitCommandError
        mock_repo = MagicMock()
        mock_repo.iter_commits.side_effect = GitCommandError("test", "test")
        repoclass.return_value = mock_repo

        with pytest.raises(repository.GitRepoError):
            repository.get_latest_commits("/test/path")


class TestCheckout():

    """
    checkout()
    """

    @patch('labs.common.git.repository.Repo')
    def test_calls_git_checkout(self, repoclass):
        mock_repo = MagicMock()
        repoclass.return_value = mock_repo

        repository.run("checkout", "main", repodir="repodir")

        mock_repo.git.checkout.assert_called_with("main")


class TestPull():

    """
    pull()
    """

    @patch('labs.common.git.repository.Repo')
    def test_calls_git_pull_origin_main(self, repoclass):
        mock_repo = MagicMock()
        repoclass.return_value = mock_repo

        repository.pull("repodir")

        mock_repo.git.pull.assert_called_with("origin", "main")


def get_repo_root_dir():
    return Path(__file__).parent.parent.parent.parent
