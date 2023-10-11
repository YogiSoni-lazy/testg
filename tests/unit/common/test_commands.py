from labs.common.commands import run_command, run_command_step


def test__run_command__returns_process():
    """
    run_command() Returns a CompletedProcess object
    """
    process = run_command("pwd")

    assert process.returncode == 0


def test__run_command_step__returns_process_and_step():
    """
    run_command_step() returns a tuple (CompletedProcess, Step)
    """
    process, step = run_command_step("My message", "pwd")

    assert process.returncode == 0


def test__run_command_step__verifies_output():
    """
    run_command_step() verifies output
    """
    process, step = run_command_step(
        "My message",
        "ls",
        options=["--help"],
        prints="list",
    )

    assert step.has_succeeded()


def test__run_command_step__shell__verifies_output():
    """
    run_command_step() verifies output
    (shell=True)
    """
    process, step = run_command_step(
        "My message",
        "ls --help",
        prints="list",
        shell=True
    )

    assert step.has_succeeded()
