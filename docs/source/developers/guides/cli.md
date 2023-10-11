# Using the `lab` CLI

The `lab` CLI implements the common verbs and manage the parsing of the command line commands, options, and arguments.
The syntax is as follows:

```console
$ lab [options] action module-name
```

:::{tip}
Create and activate a virtual environment before running lab commands
:::

## Installing the Lab Scripts of a Course

```console
$ lab install do378
```

This command installs the latest version of the `rht-labs-do378` package from [PyPI Prod](../../infrastructure/pypi).

If you are a course developer, you might want to install a specific version of the package, from PyPI Dev.

```console
$ lab install do378 --version 2.13.2 --env test
```

## Selecting the Active Course Package

Typically, you might have installed multiple course packages.
To select the module where DynoLabs must search lab scripts, use this command:

```console
$ lab select do378
```

This command sets `do378` as the lab scripts module, an stores the configuration in `~/.grading/config.yaml`

## Running Lab Scripts

Start, finish and grade lab scripts with the following commands.

```console
$ lab start hello-world
$ lab grade hello-world
$ lab finish hello-world
```

### Lab Class Resolution

Which module is loaded depends on two pieces of information:

* The course SKU that you have selected with `lab select`, e.g `do378`
* The name of the lab script, e.g. `hello-world`

When you run `lab start|grade|finish` commands, DynoLabs gets the active course module from `~/.grading/config.yaml`.
Next, DynoLabs traverses the classes of the active module (`do378` in the example) and selects the class that contains the `__LAB__` property set to `hello-world`.

Therefore, for the preceding example, you must define a class inside the `do378` module, similar to the following:

```python
# File: do378/my_ge.py
from labs.activities import GuidedExercise

class MyGE(GuidedExercise):

  __LAB__ = "hello-world"

  def start(self): # "lab start hello-world" executes this method
    ...

  def grade(self): # "lab grade hello-world" executes this method
    ...

  def finish(self): # "lab finish hello-world" executes this method
    ...

```

:::{important}
Neither the class name or the Python file name matter for resolution.
Make sure that the `__LAB__` property of the class matches the script name that you use in the `lab` command.
:::


## Logging

The `lab log` command can find and display log files.

How you use this command depends on whether DynoLabs logs to a common file or to a file per lab.
For more details see [](../../design).

If your course is configured to use a single log file, use:

```console
$ lab logs
...
```

Otherwise, you must specify the name lab script.
For example, if you have previously run `lab start my-ge`, then you can inspect the logs for `my-ge`, by using:

```console
$ lab logs my-ge
...
```

By default the `lab log` command displays the last 10 lines of a log file.
You can adjust this value with the `-n` option.

```console
$ lab logs my-ge -n 50
...
```

## Getting installed versions

```console
$ lab --version
Lab framework version: 4.6.0
Course library: rht-labs-do378
Course library version: 2.13.0
```

Prints the version of the installed core library.
It also displays the course library that is installed and selected.

## Upgrading a Course Package

```console
$ lab upgrade do378
```

Useful to upgrade to the latest course package version, for example, if a hot fix has been released.

The command is also useful to test development versions, for example:

```console
$ lab upgrade --env test --version 2.13.0.dev0+pr.997 do378
```

## Displaying System Information

```console
$ lab system-info
{
    "cpu": {
        ...
    }
}
```

This command can be useful for reporting problems.

