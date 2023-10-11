"""
Common reusable tasks.
"""
from pathlib import Path
import shlex
import warnings
import subprocess
from typing import Dict, Iterable, Tuple, Callable, Any, Union
from . import labtools
from . import labcommand
from .workspace import Workspace
try:
    from .git import config as gitconfig
    from .git import repository
except ModuleNotFoundError:
    # Git is an optional dependency
    pass

# TODO: remove this import when we drop support for deprecated elements.
# Import "labs.core.task" to keep access to the @task decorator and other
# objects from this module.
# The access to @task, TaskException, TaskFailure, TaskSuccess and TaskResult
# through this module is deprecated
import labs.core.task

# Define the type of a task
Task = Callable[[Dict], Any]


def check_workspace_exists(item: Dict):
    workspace: Workspace = item["workspace"]
    item["failed"] = not workspace.exists()


def mkdir(item: Dict):
    """
    Creates a folder

    :param item: dict containing: path
    """
    path: str = item["path"]

    result = labtools.mkdir(path)
    item.update(result)


def rmdir(item: Dict):
    """
    Removes a folder

    :param item: dict containing:path
    """
    path: str = item["path"]

    result = labtools.rmdir(path)
    item.update(result)


def check_git_config(item: Dict):
    """
    Checks if the user and the email are set in the git global config
    """

    item["failed"] = False
    item["msgs"] = []

    if not gitconfig.username():
        item["failed"] = True
        item["msgs"].append(
            {"text": "user.name not set"}
        )
    if not gitconfig.email():
        item["failed"] = True
        item["msgs"].append(
            {"text": "user.email not set"}
        )


def check_git_remote_points_to(item: Dict):
    """
    Checks whether a local repository has a remote url
    that points to remote_repo_name

    :param item: Dict containing
        repopath: absolute path of the local repository
        remote_repo_name: name of the remote repository.
            This function checks if the remoteURL includes this value
        name: name of the remote (optional)

        """
    repopath: str = item["repopath"]
    remote_repo_name: str = item["remote_repo_name"]
    name: str = item.get("name", "origin")

    tail = f"{remote_repo_name}.git"
    item["failed"] = True
    item["msgs"] = [
        {"text": f"{tail} not found in remote urls"}
    ]

    urls = []
    try:
        urls = repository.get_remote_urls(repopath, name)
    except Exception:
        urls = []

    for url in urls:
        if url.endswith(tail):
            item["failed"] = False
            item["msgs"] = []


def check_git_local_repo_exists(item):
    """
    Checks if a repository exists in a given local folder

    :param item: Dict containing
        repopath: name of the local repo folder
    """
    repopath: str = item["repopath"]

    if repository.exists(repopath):
        item["failed"] = False
        item["msgs"] = []
    else:
        item["failed"] = True
        item["msgs"] = [
            {"text": f"Repository does not exist at {repopath}"}
        ]


def grep(item):

    """
    Greps for content in a file, optionally ignoring cases.
    Fails if the content is not found

    :param item: Dict containing
        filepath
        content
        ignorecase (optional): False by default
    """

    filepath: str = item["filepath"]
    content: str = item["content"]
    ignorecase: bool = item.get("ignorecase", False)

    try:
        with open(filepath) as f:
            text = f.read()
            needle = content

            if ignorecase:
                text = text.lower()
                needle = content.lower()

            if needle in text:
                item["failed"] = False
            else:
                item["failed"] = True
                item["msgs"] = [{
                    "text": (f"{filepath} does not contain "
                                f"the following expected content: {content}")
                }]
    except OSError as error:
        item["failed"] = True
        item["msgs"] = [{
            "text": str(error)
        }]


def git(item: Dict):
    """
    Runs git commands

    :param item: Dict containing
        command: the git command as a list
        repopath
    """

    command: Iterable[str] = item.get("command", [])
    repopath: str = item["repopath"]

    try:
        repository.run(command[0], *command[1:], repodir=repopath)
        item["failed"] = False
    except repository.GitRepoError as error:
        # User tried to commit when there were no changes
        if "nothing to commit, working tree clean" in str(error).lower():
            item["failed"] = False
            item["msgs"] = [{
                "text": "Nothing to commit, skipping"
            }]
            return
        item["failed"] = True
        item["msgs"] = [{
            "text": str(error)
        }]


def check_command_result(item: Dict):
    """
    Runs a command and verifies its output and return code.

    :param item: Dict containing
        command: the git command
        cwd
        prints: Search this text in the output
        err_message: Message to use in case of error
        returns: Expected exit code
    """

    warnings.warn(
        "This function is deprecated. "
        "To run commands, "
        "use the labs.common.commands module",
        category=DeprecationWarning
    )

    command: Tuple = item["command"]
    cwd: str = item.get("cwd")
    prints: str = item.get("prints")
    returns: int = item.get("returns")
    err_message: str = item.get("err_message")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd)
    except FileNotFoundError as err:
        item["failed"] = True
        item["msgs"] = [
            {"text": str(err)}
        ]
        return item

    stdout, stderr = process.communicate()

    try:
        if returns is not None:
            assert returns == process.returncode, (
                f"Command did not exit with the {returns} code")

        if prints:
            assert prints in str(stdout), (
                f"'{prints}' not found in the command output")

        item["failed"] = False
    except AssertionError as err:
        item["failed"] = True
        item["msgs"] = []
        if err_message:
            item["msgs"].append({"text": err_message})

        item["msgs"].append({"text": str(err)})

        if stderr:
            item["msgs"].append({"text": f"Stderr: {stderr}"})


def run_command(item: Dict):
    """
    Run a command on target host(s).

    The following parameters are used:
    * ``command`` is a string with the command to be run. If the shell option
      is set to True, this string can be used to also add parameters or pipes.
    * (optional) ``options`` allows the user to add options to the command
      to be run by using an array.
    * ``host`` is the list of hosts where the command should be run
    * (optional) ``prints`` allows the user to look for a specific string at
      the stdout
    * (optional) ``returns`` allows the user to look for a specific return code
      at the output of the command
    When running in remote servers, the following parameters are used:
    * ``username`` username to execute the remote command
    * ``password`` password to authenticate the remote user
    * (optional) ``sshkey`` is the used for the ssh connection.
      Defaults to /home/student/.ssh/lab_rsa if not provided.
    * (optional) ``student_msg`` allows to provide more information to the
      students when the command exit is an error.
    * (optional) ``shell`` allows to set the subprocess shell option to true,
      executing the command through the shell. Then, the command, options,
      pipes, etc. can be given through the command option.
    """

    warnings.warn(
        "This function is deprecated. "
        "To run commands, "
        "use the labs.common.commands module",
        category=DeprecationWarning
    )

    sshkey = labcommand.check_sshkey(item)

    host_list: str = item["hosts"]

    command = item["command"]
    options = item["options"]

    shell_opt = item["shell"]
    # Note: to test that the shell parameter works correctly, I recommend using
    # a lab script that contains the following:
    #
    # steps.run_command("label", ["workstation", "servera", "serverb"],
    #                   command="echo", options=["'"]),
    #
    # This command runs with shell=False, so the ' should be properly escaped.
    # The output of running this should be a single '.
    #
    # steps.run_command("label", ["workstation", "servera", "serverb"],
    #                   command="cat /etc/passwd | grep nobody ; uptime",
    #                   shell=True),
    #
    # This command runs with shell=True, so pipes and ; should work correctly.
    # It should output something like:
    #
    # nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
    #  06:06:37 up 35 min,  1 user,  load average: 0.00, 0.00, 0.00
    #
    # Remember to test both local and remote commands.

    args = [command] + options

    output = []
    item["failed"] = False

    for target in host_list:
        target_args = args
        target_shell_opt = shell_opt
        # If running in remote server use ssh
        if (target != "localhost") and (target != "workstation"):
            user = item["username"]
            target_shell_opt = False
            if shell_opt:
                target_args = ["ssh", f"{user}@{target}", "-i", sshkey] + args
            else:
                quoted_args = list(map(shlex.quote, args))
                target_args = (
                    ["ssh", f"{user}@{target}", "-i", sshkey] +
                    quoted_args
                )

        output = labcommand.run_log(target_args,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=target_shell_opt)

        if "returns" in item:
            labcommand.check_retcode(item, output)
        if "prints" in item:
            labcommand.check_prints(item, output)

        if item["failed"] is True:
            labcommand.log_errormsg(item["msgs"])


@labs.core.task.task
def copy_lab_files(
    fromdir: Union[Path, str],
    to: Union[Path, str],
    no_source_error=True
):
    """
    Copies a directory into a destination.
    The `no_source_error` controls whether an error is raised if the source dir
    does not exist
    """
    try:
        labtools.copy_or_replace_dir(str(fromdir), str(to), no_source_error)
    except Exception as err:
        raise TaskException(["Error copying lab files to workspace", str(err)])

    return TaskSuccess([f"Lab files copied to {to}"])


# DEPRECATED
# Importing the task decorator/types from this module is deprecated.
# To prevent circular dependencies, they have been moved to `labs.core.task`
# =============

def task(func):
    warnings.warn(
        "@task has been moved to the labs.core.task module",
        category=DeprecationWarning
    )
    return labs.core.task.task(func)


# These are DEPRECATED too
TaskException = labs.core.task.TaskException
TaskResult = labs.core.task.TaskResult
TaskFailure = labs.core.task.TaskFailure
TaskSuccess = labs.core.task.TaskSuccess
