#!/usr/bin/env python3
#
# This is the main entry point for the lab grading framework.
# Execute lab --help for syntax on using this script.
#
import os
import subprocess
import sys
import logging
from typing import Optional

import click
import labs.version as ver

from labs.ui.step import StepFatalError
from labs import labconfig, labload, lablog, system, course, telemetry
from labs.environment import get_pypi_url
from labs.laberrors import LabError


def setup_for_command_execution():
    """
    Loads the config before command execution.
    Ensures that telemetry is setup.
    """
    try:
        config = labconfig.loadcfg()
        telemetry.consent.ensure(config)
        return config
    except labconfig.ConfigError as error:
        show_load_help_and_exit(error)


def show_load_help_and_exit(error):
    click.secho(error.message, fg='red')
    example = click.style('lab select SKU', bold=True)
    click.echo(
        "Use %s to load the grading library" % example)
    exit(1)


def log_error_and_exit(laberror: LabError):
    logging.exception(f"Lab script has failed due to a LabError: {laberror}")
    click.secho(
        "An error has ocurred. Check the logs for more details",
        fg="red",
        err=True
    )
    exit(1)


def print_versions_and_exit():
    """
    Print the versions of the installed core and course libraries
    """
    click.echo(f"Lab framework version: {ver.__version__}")

    try:
        config = labconfig.loadcfg()
    except labconfig.ConfigError as error:
        click.echo("No course set!", err=True)
        show_load_help_and_exit(error)

    sku = config["rhtlab"]["course"]["sku"]
    sku_version = course.get_package_version(sku)

    click.echo(f"Course library: {course.get_package_name(sku)}")

    if sku_version:
        click.echo(f"Course library version: {sku_version}")
    else:
        click.echo(
            "Error loading the course library version. "
            "Is the course library installed?",
            err=True
        )

    exit(0)


def _execute_pip_install(sku, version, env, upgrade=False):
    """Extras common code that is used to either install or upgrade
    a course dynolabs package.

    Args:
        sku (str): The course SKU
        version ([type]): [description]
        env (str): either "test" or "prod", to describe the environment for
                   installed packages.
        upgrade (bool, optional): If True, performs a `pip upgrade`.
                   Defaults to False.

    Returns:
        str: The name of the installed/upgraded package
    """
    index_url = get_pypi_url(env)
    lock_version = labconfig.get_version_lock()
    if version is None and lock_version is None:
        package = course.get_package_name(sku)
    else:
        if version is None and lock_version:
            package = '"' + course.get_package_name(sku) + lock_version + '"'
        else:
            package = course.get_package_name(sku) + '==' + str(version)

    upgrade_option = ""
    if upgrade:
        upgrade_option = " --upgrade"

    pre_packages_option = ""
    if env == "test":
        # Allow pre-release packages for a test environment.
        pre_packages_option = " --pre"

    cmd = (
        f"{sys.executable} -m pip install -qqq --no-cache-dir"
        f"{upgrade_option}{pre_packages_option}"
        f" --extra-index-url {index_url} {package}"
    )

    subprocess.check_call(cmd, shell=True)

    return package


@click.command()
@click.argument("sku", required=True)
@click.option("--force", "-f", is_flag=True,
              help="Set course library even if it is "
              "not installed (mainly for course developers).")
def select(sku, force):
    """
    Select the active course grading library.

    SKU is the course code, such as gl006
    """
    if force or labload.is_course_installed(sku):
        labconfig.setsku(sku)
    else:
        click.echo("Course %s grading library is not installed." % sku)


@click.command()
@click.argument("sku", required=True)
@click.option("--version", help="Version of the course package to load."
              " If not specified, it will default to the latest version."
              " Version is like 1.0.3")
@click.option("--uninstall", "-u", is_flag=True,
              help="Uninstall the course library before installing new one.")
@click.option("--env", default='prod', type=click.Choice(['prod', 'test']),
              help="Load grading modules from this environment."
              " This is used normally by course developers."
              " Defaults to prod.")
def install(sku, version, uninstall, env):
    """
    Install the course library.

    SKU is the course code, such as gl006
    """

    # Uninstall library with pip
    if uninstall:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall',
                                  '-y', '-q', course.get_package_name(sku)])
        except subprocess.CalledProcessError:
            pass
    # Install library with pip and version specified from proper env
    try:
        package = _execute_pip_install(sku, version, env, upgrade=False)
        print("Installed %s." % package)
        labconfig.setsku(sku.lower())
    except subprocess.CalledProcessError:
        print("Could not install course library %s as requested." % package)


@click.command()
@click.argument("sku", required=True)
@click.option("--version", help="Version of the course package to upgrade to."
              " If not specified, it will default to the latest version."
              " Version is like 1.0.3")
@click.option("--env", default='prod', type=click.Choice(['prod', 'test']),
              help="Load grading modules from this environment."
              " This is used normally by course developers."
              " Defaults to prod.")
def upgrade(sku, version, env):
    """
    Upgrade the course library.

    SKU is the course code, such as gl006
    """

    # Upgrade library with pip and version specified from proper env
    try:
        package = _execute_pip_install(sku, version, env, upgrade=True)
        print("Upgraded %s." % package)
        labconfig.setsku(sku.lower())
    except subprocess.CalledProcessError:
        print("Could not install course library %s as requested." % package)


@click.group(name='lab', invoke_without_command=True)
@click.pass_context
@click.option('--version', '-v', is_flag=True,
              help='Get lab framework version number and exit.')
def main(ctx: click.Context, version):
    """
    CLI for Red Hat Training lab grading.
    """
    if version:
        print_versions_and_exit()

    if ctx.invoked_subcommand is None:
        print("No grading command specified.")


@click.command()
@click.pass_context
@click.argument('script', type=click.STRING,
                autocompletion=labload.get_all_lab_scripts)
def start(ctx, script):
    """
    Start the lab session.

    SCRIPT is the name of the lab script.
    This variable supports tab completion.
    """

    _invoke_existing_bash(script, ctx, "start")

    try:
        config = setup_for_command_execution()
        with telemetry.session(config, "start", sys.argv):
            grading = labload.import_grading_library(config, script)
            grading.start()
    except (LabError, StepFatalError) as le:
        log_error_and_exit(le)


@click.command()
@click.argument('script', type=click.STRING,
                autocompletion=labload.get_all_lab_scripts)
def finish(script):
    """
    Finish the lab session.

    SCRIPT is the name of the lab script.
    This variable supports tab completion.
    """

    _invoke_existing_bash(script, None, "finish")

    try:
        config = setup_for_command_execution()
        with telemetry.session(config, "finish", sys.argv):
            grading = labload.import_grading_library(config, script)
            grading.finish()
    except (LabError, StepFatalError) as le:
        log_error_and_exit(le)


@click.command()
@click.argument('script', type=click.STRING,
                autocompletion=labload.get_all_lab_scripts)
def grade(script):
    """
    Grade the lab.

    SCRIPT is the name of the lab script.
    This variable supports tab completion.
    """

    _invoke_existing_bash(script, None, "grade")

    try:
        config = setup_for_command_execution()
        with telemetry.session(config, "grade", sys.argv):
            grading = labload.import_grading_library(config, script)
            grading.grade()
    except (LabError, StepFatalError) as le:
        log_error_and_exit(le)


@click.command()
@click.argument("script", type=click.STRING,
                autocompletion=labload.get_all_lab_scripts)
def fix(script):
    """
    Fix/solve the lab.

    SCRIPT is the name of the lab script.
    This variable supports tab completion.
    """

    _invoke_existing_bash(script, None, "fix")

    try:
        config = setup_for_command_execution()
        with telemetry.session(config, "fix", sys.argv):
            grading = labload.import_grading_library(config, script)
            grading.fix()
    except (LabError, StepFatalError) as le:
        log_error_and_exit(le)


def _invoke_existing_bash(script, ctx, verb):
    has_existing_bash = (script not in labload.get_classes(ctx, None, None)
                         and script in labload.get_bash_scripts())
    if has_existing_bash:
        command = ["/usr/local/bin/lab", script, verb]
        process = subprocess.run(command)
        sys.exit(process.returncode)


@click.command()
@click.argument("shell", required=False, default="bash",
                type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell):
    """
    Print completion commands for a given shell
    """
    try:
        # Get the name of the current script: "lab"
        name = os.path.splitext(os.path.basename(__file__))[0]

        # Run "_LAB_COMPLETE=<shell>_source lab" and print the result
        env = os.environ.copy()
        env["_{}_COMPLETE".format(name.upper())] = "{}_source".format(shell)
        subprocess.run(
            [name],
            timeout=1,
            env=env,
            check=False,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(e)


@click.command(name='system-info')
def system_info():
    """
    Generate a system report of the current environment.
    """
    system.report.generate("json")


@click.command(
    name="logs",
    help="Get logs for a lab script. \n\n"
    "The SCRIPT parameter is required if the course "
    "uses a log file per script, e.g. '/tmp/log/labs/exercise-one'. \n\n"
    "If the course is configured to send all logs to a single file "
    "(e.g. '/tmp/log/all-labs.log'), "
    "then omit the SCRIPT argument."
)
@click.argument(
    "script",
    required=False,
    type=click.STRING,
    autocompletion=labload.get_all_lab_scripts,
)
@click.option(
    "--lines", "-n",
    default=10,
    help="By default, display the 10 most recent lines"
)
def logs(script: Optional[str], lines: int):
    """
    Print the logs of lab script
    """
    config = labconfig.loadcfg()
    logging_config = config["rhtlab"]["logging"]

    output = []
    try:
        output = lablog.read_log_lines(logging_config, script)
    except FileNotFoundError as error:
        if script:
            click.secho(
                f"Log file for script '{script}' "
                f"does not exist ({error.filename}). "
                "Did you run the script?",
                err=True,
                fg="red"
            )
        else:
            click.secho(
                f"The '{error.filename}' logging path does not exist"
                "Verify the '~/.grading/config.yaml' file",
                err=True,
                fg="red"
            )

        sys.exit(1)
    except IsADirectoryError as error:
        if script:
            click.secho(
                f"The '{error.filename}' logging path is a directory "
                "due to invalid configuration."
                "Verify the '~/.grading/config.yaml' file",
                err=True,
                fg="red"
            )
        else:
            click.secho(
                f"The '{error.filename}' logging path is a directory.\n"
                "Specify a script name that exists "
                "as a file in the log directory, "
                "via the 'lab logs SCRIPT' command.\n"
                "The available options are: \n",
                fg="yellow"
            )
            for filename in os.listdir(error.filename):
                click.secho(f"\tlab logs {filename}", fg="yellow")

        sys.exit(1)

    tail = output[-lines:]
    click.echo("".join(tail))


main.add_command(finish)
main.add_command(grade)
main.add_command(start)
main.add_command(fix)
main.add_command(select)
main.add_command(install)
main.add_command(upgrade)
main.add_command(completion)
main.add_command(system_info)
main.add_command(logs)


if __name__ == "__main__":
    main()
