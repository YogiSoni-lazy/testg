# Quick Start

With DynoLabs, each course must bundle (and distribute) the course lab scripts in a Python package.
For example, the DO378 lab scripts are available in a package called `rht-labs-do378`.

Moreover, for the DynoLabs `lab` command to be able to resolve lab scripts, the course package must expose a module named as the course SKU.
For example, for DO378, the `rht-labs-do378` package exposes a module called `do378`.

To generate the configuration and the files required to define the Python package for a course, you can use the `lab-generator` tool, which is included in the DynoLabs core repository.

## Installing `lab-generator`

Pull the `https://github.com/RedHatTraining/rht-labs-core` repository.

Change to the root of the `rht-labs-core` local repository.

Activate a virtual environment with `rht-labs-core` installed.
For example:

```console
$ python3 -m venv .venv    # Create the venv. Only necessary if the .venv virtualenv does not exist yet
$ . .venv/bin/activate     # this activates the virtualenv; your prompt should change, adding (.venv). This is necessary for running anything in the virtualenv
(.venv) $ pip install -e . # this is only necessary for the initial setup of the virtualenv. This installs rht-labs-core in editable mode to the virtualenv
```

Then run:

```console
$ pip install generator/
```

This command installs `lab-generator` in the `rht-labs-core` virtual environment.

## Generating the Python Package for a Course

:::{important}
Ignore this step if your course already defines a Python package at `classroom/grading/`.
:::

Lab package generation is needed for new courses or for migrating courses from bash.

To generate a lab package for a course, execute the `lab-generator` tool with the `create-package`
option, the course SKU as the first parameter and the path of the course git repository as the
second parameter.
You must create the lab scripts in the `classroom/grading` subdirectory of the course repository.

```console
(.venv) $ lab-generator create-package <SKU> <PATH_TO_COURSE_GIT_REPOSITORY>/classroom/grading
```

E.g. for DO370:

```console
(.venv) $ lab-generator create-package DO370 /home/GLS/DO370/classroom/grading
Creating directory: /home/GLS/DO370/classroom/grading
Creating labs package for DO370
Lab package is located in the: /home/GLS/DO370/classroom/grading directory
```

This command generates a structure similar to the following:

```shell
DO378/classroom/grading
├── MANIFEST.in         # Specifies additional files to include in the package
├── README.md           # do378 package docs
├── setup.cfg           # Package definition file
├── setup.py            # Entrypoint for package defition file
└── src                 # Source code dir
    └── do370           # do378 Python module
        ├── __init__.py # do378 Python module initialization file
        └── version.py  # package version file
```

You must add your scripts in the `src/do378` directory.

Note that, if you inspect the `setup.cfg` file, the DynoLabs core library is listed as a dependency.

```
install_requires =
    rht-labs-core~=4.7.0
```

## Initializing the Python Package for a Course

:::{important}
Make sure you follow these steps when you start working on a course that already defines a Python package at `classroom/grading/`.
:::

Before you start working on the course lab scripts, you must create a Python virtual environment, specific for the course, and install the dependencies of the course package, which are specified in `setup.cfg`.

First, deactivate the `rht-labs-core` virtual environment in your terminal:

```console
(.venv) $ deactivate
$
```
Or, alternatively, open a new terminal.
You must use a specific virtual environment for each course.


Next, create a new virtual environment for the course, and activate the environment (in this example, for `do378`):

```console
$ python3 -m venv ~/venvs/do370  # Create a venv in ~/venvs/do370
(do370) $ source ~/venvs/do370/bin/activate  # Activate the venv
```

Next, navigate to the `classroom/grading` directory of the course and install the dependencies of the Python package.
Initially, the package only depends on `rht-labs-core`, but you can add more dependencies if needed.

```console
(do370) $ cd ~/courses/do370/classroom/grading # Move to the course lab scripts directory
(do370) $ pip install -e . \
 --extra-index-url https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple # Install the dependencies of the setup.cfg file
```

Now that DynoLabs is installed, you can use the `lab` command.

Finally, set the DynoLabs active course.
This is a requirement in DynoLabs.
You must select the active course, so DynoLabs can locate the module that contains the lab scripts.

```console
(do370) $ lab select do370  # Creates the ~/.grading/config.yaml file, which is the main DynoLabs config file
```

In this example, we select the `do370` module as the active module.
When you run a script, for example with `lab start`, DynoLabs will resolve scripts by looking into this module.

You are now ready to create and execute lab scripts.

## Generating Lab Scripts

When the lab package has been generated or if the package already exists,
use the `lab-generator` tool with the `add-script` option with the SKU,
git repository and script name as mandatory parameters.

To use `lab-generator` you must be in the `rht-labs-core` virtual environment.

```console
(.venv) $ lab-generator add-script <SKU> <PATH_TO_COURSE_GIT_REPOSITORY>/classroom/grading <lab-name>
```

E.g. For DO370:

```console
(.venv) $ lab-generator add-script DO370 /home/GLS/DO370/classroom/grading install-setup
The new lab script is located at /home/GLS/DO370/classroom/grading/src/do370/install-setup.py
```

After the script has been generated, activate the course virtual environment.
You can now run the `start`, `finish` or `grade` actions of the newly created `install-setup` script.

```console
(do370) $ lab start install-setup

Starting lab.
```
## Next Steps

Start [](./guides/implementing.md).
