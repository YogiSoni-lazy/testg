"""
Podman commands.
"""

from enum import Enum
from os import environ
from shutil import which
from typing import List, Optional

from labs.common.commands import run_command


class PodmanCommands:
    MAIN = "podman"
    REMOVE = "rm"
    STOP = "stop"
    IMAGE = "image"
    IMAGES = "images"
    NETWORK = "network"
    KILL = "kill"
    RUN = "run"
    LOGIN = "login"
    PORT = "port"
    EXECUTE = "exec"
    VOLUME = "volume"


class PodmanRegistries(Enum):
    CLASSROOM = "registry.ocp4.example.com:8443"
    QUAY = "quay.io"


def exists() -> bool:
    return which(PodmanCommands.MAIN) is not None


def run_container(
    name: str, image: str, opts: Optional[List[str]] = None
):
    if opts is None:
        opts = []
    if environ.get("DEV_LOCAL", "false").lower() == "true":
        opts.append("--tls-verify=false")
    return _execute_command(
        [PodmanCommands.RUN, *opts, f"--name={name}", image]
    )


def return_running_containers(
    format: Optional[str] = None
):
    args = [] if not format else [f'--format="{format}"']

    return _execute_command(["ps"] + args)


def return_volume_exists(name: str):
    return _execute_command([PodmanCommands.VOLUME, "exists", name])


def kill_container(name: str):
    return _execute_command([PodmanCommands.KILL, name])


def execute_in_container(
    container: str, cmd: List[str], opts: Optional[List[str]] = None
):
    if opts is None:
        opts = []
    return _execute_command([PodmanCommands.EXECUTE, *opts, container, *cmd])


def remove_all_containers():
    return _execute_command([PodmanCommands.REMOVE, "--all"])


def remove_specified_container(
    name: str, force: bool = False
):
    return _execute_command(
        [PodmanCommands.REMOVE, name] + (["-f"] if force else [])
    )


def remove_volume(name: str):
    return _execute_command([PodmanCommands.VOLUME, "rm", name])


def prune_volumes():
    return _execute_command([PodmanCommands.VOLUME, "prune", "-f"])


def check_if_authorized(registry: PodmanRegistries):
    return _execute_command(
        [PodmanCommands.LOGIN, "--get-login", registry.value]
    )


def classroom_registry_login(user="developer", password="developer"):
    return _execute_command(_get_login_cmd(user, password))


def _get_login_cmd(user: str, password: str):
    command = [
        PodmanCommands.LOGIN,
        PodmanRegistries.CLASSROOM.value,
        "-u",
        user,
        "-p",
        password
    ]
    if environ.get("DEV_LOCAL", "false").lower() == "true":
        command.append("--tls-verify=false")
    return command


def stop_specified_container(container):
    return _execute_command([PodmanCommands.KILL, container])


def stop_all_containers():
    return _execute_command([PodmanCommands.STOP, "--all"])


def return_all_containers(format_out: str = ""):
    return _execute_command(
        ["ps", "--all"] + ([] if not format else [f'--format="{format_out}"'])
    )


def return_container_ports(container: str):
    return _execute_command([PodmanCommands.PORT, container])


def return_all_container_ports_in_use():
    return _execute_command([PodmanCommands.PORT, "--all"])


def return_all_container_images():
    return _execute_command([PodmanCommands.IMAGES])


def inspect_image(image, format=""):
    return _execute_command(["image", "inspect", image, f'-f "{format}"'])


def prune_images():
    return _execute_command([PodmanCommands.IMAGE, "prune", "-a", "-f"])


def inspect_container(container: str, format=""):
    return _execute_command(["inspect", container, f'-f "{format}"'])


def return_all_networks():
    return _execute_command([PodmanCommands.NETWORK, "ls", "--noheading"])


def return_all_volumes():
    return _execute_command([PodmanCommands.VOLUME, "ls", "--noheading"])


def remove_specified_network(network: str):
    return _execute_command([PodmanCommands.NETWORK, "rm", network])


def _execute_command(
    options: List[str], sudo: bool = False
):
    if sudo:
        return run_command("sudo", [PodmanCommands.MAIN] + options)
    else:
        return run_command(PodmanCommands.MAIN, options)


def create_network(network):
    return _execute_command([PodmanCommands.NETWORK, "create", network])
