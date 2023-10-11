"""
Example of labs.common.commands usage to run commands
"""
from labs.ui import Step
from labs.common.commands import run_command_step, run_command
from labs.activities import GuidedExercise


class ExamplePythonCommands(GuidedExercise):

    __LAB__ = "python-commands"

    def start(self):

        # You can run commands like:

        run_command_step(
            "A step that runs 'ls -l'",
            "ls", ["-l"]
        )

        run_command_step(
            "A step that verifies that 'ls -l' output contains hello",
            "ls", ["-l"],
            prints="hello"
        )
        run_command_step(
            "A step that verifies that 'ls -l' output contains hello "
            "(Shell=True)",
            "ls -l",
            prints="hello",
            shell=True
        )

        run_command_step(
            "A step that verifies that 'ls -l' returns 0",
            "ls", ["-l"],
            returns=0
        )

        run_command_step(
            "A step that verifies that 'ls -l' with shell=True returns 0",
            "ls -l",
            shell=True,
            returns=0
        )

        # Or you can build your own custom steps

        with Step("Checking substrings of `hello`", fatal=False) as step:

            # "run_command" is a regular Python function
            #
            # In many cases, you can use "run_command_step",
            # which wraps "run_command" in a UI Step, and takes care
            # of the UI output/messaging for you
            #
            # When you need finer control, for example,
            # to combine multiple commands,
            # you can use the "run_command" function

            process = run_command("echo hello | grep bye", shell=True)

            if process.returncode != 0:
                step.add_message("Hello does not contain `bye`")

                process = run_command("echo hello | grep o", shell=True)

                if process.returncode == 0:
                    step.add_message("But hello contains `o`")

    def finish(self):
        pass
