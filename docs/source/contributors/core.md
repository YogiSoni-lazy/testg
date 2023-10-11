# Contributing to `rht-labs-core`

## Set up the Development Environment

- Clone `github.com/RedHatTraining/rht-labs-core`.

- Make sure Python 3.6 or higher is installed.

- Create a private Python virtual environment for development.

- Activate the newly created Python virtual environment.

``` console
[user@host ~]$ cd rht-labs-core
[user@host rht-labs-core]$ make venv
[user@host cd rht-labs-core]$ source ~/.venv/labs/bin/activate
(labs) [user@host cd rht-labs-core]$
```

:::{note}
The `venv` target of the `Makefile` also installs the `requirements.txt`
so you will have all the packages you need to do development.
:::

- Install `rht-labs-core` and `rht-labs-gl006` packages as development
  packages using `pip`. Note the special syntax for `pip`. You are not
  installing a prebuilt package like you normally do with `pip`.

``` console
(labs) [user@host ~]$ cd rht-labs-core
(labs) [user@host rht-labs-core]$ pip install --editable .
(labs) [user@host rht-labs-core]$ cd packages-gl006
(labs) [user@host packages-gl006]$ pip install --editable .
```

:::{note}
You must have your Python virtual environment activated before you run
these commands.

The script `bootstrap/workstation/dev_boostrap.sh` performs this basic
setup tasks.
:::

- Create a configuration file for local development of the sample course
  `gl006`:

``` console
(labs) [user@host rht-labs-core]$ lab load gl006 --local
```

- Test your development setup:

``` console
(labs) [user@host rht-labs-core]$ lab start example-python
```

## Tab Completion

The lab framework supports tab completion. Install the
`rht-labs-core/lab-completion.sh` file in `etc/bash_completion.d/` or
the appropriate location for your OS. Reload your bash session and you
should be able to use tab completion with the `lab` command.

## Shell Lab Scripts Support

If traditional shell lab scripts are present in the system, then
`rht-labs-core` supports running them. Before running a lab script,
`rht-labs-core` looks for `/usr/share/bash-completion/completions/lab`.
If that file exists, then `rht-labs-core` assumes that it is running on
a system with traditional shell scripts. `rht-labs-core` then checks
`content.example.com` to list the available lab scripts (very much like
the traditional lab completion script works). If the user tried to
execute a script that is not present on the course DynoLabs package, but
which is present on the traditional lab scripts, then `rht-labs-core`
executes the existing lab script.

Tab completion should show both DynoLabs and traditional lab scripts.

Note that traditional lab scripts use `lab lab-name verb` instead of
`lab verb lab-name`. If you are using this feature, then you should
replace mentions of `lab lab-name verb` with `lab verb lab-name` in the
student guide.

## Checking code style

This project follows the [PEP8 style guide for
Python](https://www.python.org/dev/peps/pep-0008/). The style is
enforced with the [flake8](https://flake8.pycqa.org/en/latest/) linter.
To run the check, execute:

``` console
(labs) [user@host rht-labs-core]$ make lint
```

You can also run flake8 with:

``` console
(labs) [user@host rht-labs-core]$ flake8 .
```

`flake8` is configured in the `[flake8]` section of the `setup.cfg`
file.

**Code style linting is part of the CI pipeline.**

## Running tests

To run the tests, execute:

``` console
(labs) [user@host rht-labs-core]$ make test
```

:::{note}
Integration tests use the `rht-labs-ts000` example course project. You
can find the source code of this module in `tests/testcourse`.

The `requirements.txt` file of `rht-labs-core` is already configured to
install this module as a local dependency. If for some reason this
package is not available in your environment, run
`pip install -r requirements.txt` at the root of the repository.
:::

This command uses the [`pytest`](https://docs.pytest.org/en/stable/)
framework. You can also run tests directly invoking `pytest`:

``` console
(labs) [user@host rht-labs-core]$ python -m pytest
```

The `-m` parameter invokes `pytest` as a module, adding the current
working directory to `sys.path`. This is to allow `pytest` to find
modules in the `src/` folder.

Tests are located in the `tests/` directory. Add new tests to this
folder.

**Tests are part of the CI pipeline.**

## Contributing to the Documentation

You can directly commit changes to the files under `docs/source`.
Jenkins will rebuild and publish the updated documentation.

:::{tip}
Use the _pencil_ icon at top of the page to edit the documentation.
:::

If you want to preview the HTML locally, then you need `Shpinx`, which is the documentation engine used to generate this docs.

To install the `Sphinx` and the other requirements to create the docs, you might want to create a specific virtual environment and install the dependencies:

```console
[user@host rht-labs-core]$ python3.9 -m venv .venvdocs
[user@host rht-labs-core]$ source .venvdocs/bin/activate
(.venvdocs)[user@host rht-labs-core]$ cd docs
(.venvdocs)[user@host docs]$ pip install -r requirements.txt
```

Now, you can generate the HTML as follows:

```console
(.venvdocs)[user@host docs]$ make html
...output omitted...
build succeeded, 7 warnings.

The HTML pages are in build/html.
```

Sphinx builds the HTML output at `docs/build/html`.



