import logging
import pathlib
import pprint
import textwrap
import typing

import pkg_resources

import ansible_runner

from labs.ui import Step, GradingStep


def run_playbook_step(exercise_class, playbook: str, grading: bool = False,
                      tags: typing.List[str] = None,
                      extra_vars: typing.List[str] = None,
                      extra_args: typing.List[str] = None,
                      inventory: str = "inventory",
                      directory: str = "ansible",
                      expected_error_prefix: str = "· ",
                      step_message: str = "Running playbook"):
    """Runs a playbook as a step.

    :param exercise_class: pass "self" here
    :param directory: paths are relative to the exercise_class and this
        directory
    :param expected_error_prefix: prefix playbook messages with this string, so
        they are considered "expected" errors, and displayed more nicely.

    See :doc:`/developers/guides/ansible`.

    """

    step_type = GradingStep if grading else Step

    with step_type(step_message) as step:
        path = _get_path(exercise_class, directory)
        envvars = {
            "ANSIBLE_CONFIG": str(path / "ansible.cfg"),
        }
        cmdline = ""
        if extra_args:
            cmdline += extra_args
            cmdline += " "
        if tags:
            for tag in tags:
                cmdline += f"--tags {tag} "
        if extra_vars:
            double_quote = '"'
            for var, value in extra_vars.items():
                if double_quote in value:
                    cmdline += f"-e {var}='{value}' "
                else:
                    cmdline += f'-e {var}="{value}" '

        config = ansible_runner.runner_config.RunnerConfig(
            private_data_dir=path,
            playbook=playbook,
            inventory=str(path / inventory),
            cmdline=cmdline.strip(),
            envvars=envvars,
        )
        config.prepare()
        config.suppress_ansible_output = True
        runner = ansible_runner.Runner(config=config)
        runner.run()

        if runner.rc == 0:
            logging.info("Ran playbook %s successfully", playbook)
            return

        expected_messages, unexpected_messages = _extract_messages(
            runner,
            expected_error_prefix)

        if expected_messages:
            step.add_errors(expected_messages)
        else:
            step.add_errors(unexpected_messages)
            step.add_error(_generate_troubleshooting_error(
                path, playbook, cmdline))


def _extract_messages(runner, expected_error_prefix):
    failed_events = [e
                     for e in runner.events
                     if e["event"] == "runner_on_failed"]

    unexpected_messages = []
    expected_messages = []

    for event in failed_events:
        logging.error("Failed event %s", pprint.pformat(event))
        initial_message = event["event_data"]["res"]["msg"]
        if isinstance(initial_message, list):
            messages = initial_message
        else:
            messages = [initial_message]

        for loop_msg in messages:
            expected, message = _process_message(event,
                                                 loop_msg,
                                                 expected_error_prefix)
            if expected:
                expected_messages.append(message)
            else:
                unexpected_messages.append(message)

    return set(expected_messages), unexpected_messages


def _process_message(event, message, expected_error_prefix):
    if message.startswith(expected_error_prefix):
        return True, message.replace(expected_error_prefix, '')

    host = event["event_data"]["host"]
    task = event["event_data"]["task"]
    msg = event["event_data"]["res"]["msg"]

    return False, f"{host}: {task}: {msg}"


def _get_path(exercise_class, path):
    return pathlib.Path(
        pkg_resources.resource_filename(exercise_class.__module__, path)
    )


def _generate_troubleshooting_error(path, playbook, cmdline):
    ruler = "-" * 80
    return textwrap.dedent(
        f"""
        Troubleshoot the failed playbook with:
        {ruler}
        $ cd {path}
        $ ansible-playbook {playbook} -i inventory {cmdline}
        {ruler}
        """
    ).strip()
