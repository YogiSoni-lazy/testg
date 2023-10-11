# Creating the Lab Script Package in a Course

## Option 1: Use the `lab-generator` Tool

Follow the instructions at the [](../quickstart.md) guide.

## Option 2: Create the Files Manually

You should create the Python package at `classroom/grading`.

* The `Makefile`, `setup.cfg`, etc. go in this directory.
* The course Python module begins at  `classroom/grading/src/<sku>`.
  * Or, alternatively, at  `classroom/grading/<sku>`.
  * The `ansible`, `common` directories belong here.
  * The lab scripts belong at this level for all scripts, e.g `classroom/grading/<sku>/test_unit.py`.
  * Course-specific shared libraries also belong here, e.g. `classroom/grading/<sku>/lib/kafka.py`.

For an example, see [DO378](https://github.com/RedHatTraining/DO378/tree/main/classroom/grading).