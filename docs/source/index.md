# DynoLabs Documentation

*DynoLabs* is the set of Python libraries used at Red Hat Training for implementing scripts in guided exercises and labs.
These scripts are used to set up and clean up the scenario for each exercise, as well as grading the student's work.

## Quick Intro

{{core_version_badge}}

The core of DynoLabs is implemented in [`rht-labs-core`](https://github.com/RedHatTraining/rht-labs-core).
Some of the most important features of this library are:

* The `lab` CLI, which provides commands to run lab scripts and manage packages.
* A Python module to create lab scripts with Ansible and Python.
* A Python module of reusable routines to perform common tasks, such as copying files or running commands.

Other DynoLabs libraries implement specific tools for lab scripts to interact with particular technologies, such as [`rht-labs-ocpcli`](https://github.com/RedHatTraining/rht-labs-ocpcli), which provides tools to interact with OpenShift via the `oc` CLI.

Each course also implements a Python library, which contains the lab scripts specific to the course.
These libraries are typically called `rht-labs-<sku>`.

The DynoLabs libraries are not available at [PyPI.org](https://pypi.org/).
Instead, we use our own [PyPI servers](infrastructure/pypi.md).

For more details about the design of DynoLabs, see [](design).

## Example

**What You Implement**

```python
from labs.activities import Lab
from labs.common.commands import run_command_step


class MyLovelyExercise(Lab):

    __LAB__ = "example-lab"

    def start(self):
        run_command_step(
            "A step that runs 'ls -l'",
            "ls", ["-l"]
        )
        run_command_step(
            "A step that verifies that 'ls -l' output contains hello",
            "ls", ["-l"],
            prints="hello"
        )
```

**What You Invoke**

```console
$ lab start example-lab
SUCCESS A step that runs 'ls -l'
FAIL    A step that verifies that 'ls -l' output contains hello
        - 'ls' did not print the expected message
        - 'hello' not found in command output
```


## For Course Developers

Read these guides if you are a course developer who uses DynoLabs to write lab scripts.

```{toctree}
:maxdepth: 2

developers/quickstart
developers/guides/README
developers/training/README
```

## For Contributors

For the maintainers of `rht-labs-core` and other DynoLabs libraries.

```{toctree}
:maxdepth: 2

contributors/README
```

## For Infrastructure Engineers

```{toctree}
:maxdepth: 2

infrastructure/README
```

## For Instructors

```{toctree}
:maxdepth: 2

instructors/README
```


## DynoLabs Architecture

```{toctree}
:maxdepth: 2

design
```

## API

Specific documentation on functions, classes, and methods

```{toctree}
:maxdepth: 2

api
```


# Indices and tables

* [](genindex)
* [](modindex)
