# DynoLabs Architecture

## DynoLabs Components

The major components of DynoLabs are implemented as Python packages:

### The Core Package

**A.k.a `rht-labs-core`**

The DynoLabs core package, which includes:

1. Entry point for the `lab` CLI.
2. Abstracts classes in {py:mod}`labs.activities` to define the start, finish and grade actions for each exercise.
3. Logging Features.
4. DynoLabs system-wide configuration.

### Packages by Product

**A.k.a `rht-labs-<product>` packages** 

Utility packages by product.

These packages  implement common functionality module(s) for a particular product, e.g. `rht-labs-ocpcli`, which uses  the `oc` CLI to perform actions in OpenShift clusters.

### Packages by Course

**A.k.a  `rht-labs-<sku>` packages**

Each course publishes a Python package to our PyPI servers.
The course-specific lab scripts are implemented in these packages.

Course packages must depend on `rht-labs-core`.
Lab scripts are implemented by implementing the abstract classes from the {py:mod}`labs.activities` in `rht-labs-core`.

Course packages can optionally use `rht-labs-<product>` packages.
For example, if the grading scripts of your course require interaction with OCP, you might want to install `rht-labs-ocpcli` in your course package.


## The `lab` CLI

The CLI consists of a `lab` shell script for backwards compatibility which invokes `lab.py`
that does the actual work.

`lab.py` is the controller of the CLI with which the student interacts, and provides the following functions:

* Syntax control of the commands on the command line
* Providing help with the command syntax on the command line
* Dynamically loading the lab module library
* Invoking the various verbs supported by the "lab script"

For more information about the use of the CLI, see [](developers/guides/cli)

## DynoLabs Configuration

DynoLabs uses a YAML configuration file to define the currently active course module, and the logging path.
By default, the configuration file is `~/.grading/config.yaml`.

The `labs.labconfig` module is in charge of loading and saving this file.
For example, when you run `lab select SKU`, it sets the active SKU module in the configuration file (and creates the file if it does not exist).
Also, when you run lab control commands such as `lab start`, the `lab.labconfig` module parses the configuration from this file

### Sample Configuration File

```yaml
rhtlab:
  course:
    sku: XX000
    version: 0
  logging:
    level: debug
    path: /var/log/rht-lab/
```


## Logging

When you invoke `lab` commands, DynoLabs configures a Python logger to send logs to the `rhtlab.logging.path` set in the configuration file.

You can also set the logging level with the `rhtlab.logging.level` of the configuration file.

To generate logs, you can use the default Python `logging` module and its functions, such as `logging.info` to produce logs with the specific DynoLabs logging configuration.

### Log Files and Directories

If `rhtlab.logging.path` ends with `/`, then DynoLabs treats this path as a directory.

For example, if you set this value to `/tmp/log/labs/` and you run `lab start my-ge`, then DynoLabs logs to the `/tmp/log/labs/my-ge` file.

If you set the logging path to `/tmp/log/labs` (without the trailing `/`), then DynoLabs writes all logs to the  `/tmp/log/labs` file.

## Course-specific Lab Script Packages

To run lab scripts, DynoLabs requires this scripts to be defined as subclasses of the {py:class}`labs.activities.GuidedExercise` or {py:class}`labs.activities.Lab` classes.
To group and release these classes by course, the recommendation is to create the Python package for lab scripts under the `classroom/grading` directory of the course repository, by using the typical Python package structure.
The structure should similar to this example:

```bash
~/courses/DO378/classroom/grading
├── do378 # The course-specific lab scripts module
│   ├── __init__.py
│   ├── lib # Common functionality for the lab scripts of this course
│   │   ├── __init__.py
│   │   ├── steps.py
│   │   └── ...
│   ├── chapter1_section1.py # A lab script
│   ├── chapter1_section2.py # Another lab script
│   ├── chapter2_section1.py # Another one
│   ├── ...
│   └── version.py # The rht-labs-do378 package version
├── LICENSE
├── Makefile
├── MANIFEST.in # Additional files to use in the package
├── README.md
├── setup.cfg # Package config file, including dependencies (such as rht-labs-core)
├── setup.py
├── requirements.txt # Additional packagehttps://github.com/RedHatTraining/DO378/tree/main/classroom/grading dependencies for develompent (pytest...)
└── tests
    ├── __init__.py
    ├── conftest.py
    └── ...
```

For more information about creating the Python Package, see:
* [](developers/quickstart)
* [](developers/guides/creating)



## Versioning and Packaging

There are three component versions:

* The `rht-labs-core` version
* The version of DynoLabs product tooling libraries, such as [`rht-labs-ocpcli`](https://github.com/RedHatTraining/rht-labs-ocpcli)
* The version of the course-specific grading library, e.g. [`rht-labs-do378`](https://github.com/RedHatTraining/DO378/tree/main/classroom/grading)

Due to the nature of intellectual property, our modules are not
be stored on public pip repositories.
Instead we publish the DynoLabs packages in custom PyPI servers.

For more information, see [](infrastructure/pypi).

### Packaging scheme

There are three types of packages:

- Lab framework core named `rht-labs-core` with a `MAJOR.MINOR.PATCH` versioning scheme, following [PEP 440](https://peps.python.org/pep-0440/).

- Lab course library named `rht-labs-<sku>` with a `MAJOR.MINOR.PATCH` versioning scheme, where `MAJOR.MINOR` matches the course product version and the `PATCH` portion is used to release new versions of the lab scripts under the same product version.

- Lab product library named `rht-labs-<productid>` with a `MAJOR.MINOR.PATCH` versioning scheme, following [PEP 440](https://peps.python.org/pep-0440/).


### Twine

DynoLabs packages are published to our PyPI servers with `twine`.

You must set the `PS_PASSWD` (or `PS_PASSWD_PROD`) variable and export it from
`~/.bash_profile` or a similar location.
This is used in the `Makefile` to pass the password for
the `htpasswd` authentication scheme used in the PyPI server implementation.

:::{note}
Jenkins takes care of publication, so typically you do not need to deal with passwords, `Makefile`, or publishing details.
:::
