# Running Commands from Lab Steps

You can run commands by using the {py:mod}`labs.common.commands` module in your
lab scripts.

## Executing a Step that Runs a Command

Use the {py:func}`labs.common.commands.run_command_step` function in any of the `start()`, `grade()`,
or `finish()` methods of a lab script. For example:

``` python
from labs.activities import GuidedExercise
from labs.common.commands import run_command_step


class MyLabScript(GuidedExercise):

    def start(self):
        run_command_step(
            "A step that runs 'ls -l'",  # 1
            "ls",  # 2
            ["-l"]  # 3
        )
```

1. The step label
2. The command
3. The command arguments

The preceding code runs the `ls -l` command and produces the following
output:

```console
SUCCESS A step that runs 'ls -l'
```

## Running a Command and Verifying its Return Code and Output

You can use `run_command_step` to run a command and validate the result.

``` python
def grade(self):
    run_command_step(
        "A step that verifies that 'ls -l' output contains hello",
        "ls", ["-l"],
        prints="hello",  # 1
        returns=0  # 2
    )
```

1. Verifies that the command output contains `hello`
2. Verifies that the command return code is `0`

Running the preceding grading script produces the following output:

```console
FAIL    A step that verifies that 'ls -l' output contains hello
        - 'ls' in 'localhost' did not print the expected message
        - 'hello' not found in command output
```

## Executing a Step that Runs a Command on Remote Hosts

See [](ansible).

## Finer Control of Steps that Run Commands

If you need to run a command without the step UI logic, then you can use
the {py:func}`labs.common.commands.run_command` function. This function runs a command and returns an
instance of {py:class}`subprocess.CompletedProcess`.

This is useful, for example, to embed multiple commands in a single
step. For example:

``` python
from labs.ui import Step
from labs.activities import GuidedExercise
from labs.common.commands import run_command


class MyLabScript(GuidedExercise):

    ...

    def start(self):
        with Step("Checking substrings of `hello`", fatal=False) as step:
            process1 = run_command("echo hello | grep bye", shell=True)  # 1

            if process1.returncode > 0:  # 2
                step.add_message("Hello does not contain `bye`")

                process2 = run_command("echo hello | grep o", shell=True)

                if process2.returncode == 0:
                    step.add_message("But hello contains `o`")
```

1. The `run_command` function returns a `CompletedProcess` object.
2. The return code of the process is available in the `returncode`
  property. You can also use the `stdout` and `stderr` properties to get
  the command output.

The script produces this output:

```console
SUCCESS Checking substrings of 'hello'
        - Hello does not contain 'bye'
        - But hello contains 'o'
```

## Examples

For more examples, see <repo:packages-gl006/src/gl006/example-python-commands.py>.
