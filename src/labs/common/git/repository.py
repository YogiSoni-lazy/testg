from typing import List
from git import Repo
import git.exc


def exists(repodir):
    try:
        _get_repo(repodir)
        return True
    except GitRepoError:
        return False


def clone(remote: str, to_local_path: str):
    Repo.clone_from(remote, to_local_path)


def has_remote(repodir, remote_name):
    repo = _get_repo(repodir)
    return hasattr(repo.remotes, remote_name)


def get_remote_urls(repodir, remote_name="origin") -> List[str]:
    repo = _get_repo(repodir)
    try:
        return list(getattr(repo.remotes, remote_name).urls)
    except AttributeError:
        return []


def get_branches(repodir):
    repo = _get_repo(repodir)
    return [b.name for b in repo.branches]


def get_latest_commits(repodir, branch=None):
    repo = _get_repo(repodir)
    if not branch:
        branch = repo.head
    try:
        return list(repo.iter_commits(branch, max_count=50))
    except git.exc.GitError as err:
        raise GitRepoError(
            f"An error ocurred when getting commits from {repodir}"
        ) from err


def run(command: str, *args, repodir: str):
    """
    Run git command
    """
    repo = _get_repo(repodir)

    try:
        funct = getattr(repo.git, command)
        return funct(*args)
    except git.exc.GitError as err:
        raise GitRepoError(
            f"An error ocurred when runing '{command}' at {repodir}"
        ) from err


def pull(repodir: str, origin="origin", branch="main"):
    run("pull", origin, branch, repodir=repodir)


def _get_repo(repodir):
    try:
        return Repo(repodir)
    except git.exc.GitError as err:
        raise GitRepoError(
            f"An error ocurred when getting the repository at {repodir}"
        ) from err


class GitRepoError(Exception):

    """ Thrown if there are errors in this module """

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f"{self.message} -> {repr(self.__cause__)}"
