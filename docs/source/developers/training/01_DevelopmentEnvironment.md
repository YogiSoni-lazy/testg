# Establishing the Development Environment

## Concepts

There are two modes of using the grading framework:

**Development Mode**
This mode is used by developers to create lab scripts and common
functions. In this mode the developer can easily test their updates
without packaging and distributing the Python packages to the PyPI
server. Most development should be done in this way until the developer
is ready for end user testing.

**Student Mode**
This mode is the way in which the student will use the framework. The
student uses `pip` to install a course package, which will install the
core framework as well. The student may also refresh the lab environment
by installing updates to a given course with the `lab upgrade` command.
Developers should only use this mode when doing end user testing of
their code.

### Development Mode

The developer clones the source repositories needed for the framework
onto their development platform. The development platform could be a
working classroom image if the development requires a particular set of
servers or setup to test the scripts. When using a classroom workstation
it is imperative that you save your work frequently by committing the
source to your GitHub branch.

When working with local source code, we use `pip` to install a
development (editable) copy of the `rht-labs-core` and the example
`rht-labs-gl006` packages. This allows other Python modules to find
modules in the core, product, and course libraries upon which your
project is dependent. This also allows you to run the framework as if it
were installed from a package and being able to edit the code to add new
features or fix bugs.

Follow this guided exercise to acquaint yourself with the development
environment and to setup your local development environment.

## Guided Exercise 1.1

1.  Create an isolated Python virtual environment.

    1.  Check out the source code for the core library.

            [user@host ~]$ git clone git@github.com:RedHatTraining/rht-labs-core.git
            [user@host ~]$ cd rht-labs-core

    2.  Install the `make` package if necessary.

            [user@host rht-labs-core]$ which make || sudo dnf -y install make

    3.  Create the virtual environment with `make`.

            [user@host rht-labs-core]$ make venv
            python3 -m venv ~/.venv/labs && \
            source ~/.venv/labs/bin/activate && \
              pip3 install --upgrade pip > pip-log.txt && \
              pip3 install -r requirements.txt >> pip-log.txt && \
            deactivate
            All done, execute 'source ~/.venv/labs/bin/activate' to enter the venv

        <div class="note">

        To perform this exercise again, you must delete the virtual
        environment directory. You can perform this operation manually
        or use the `make distclean` command.

            [user@host rht-labs-core]$ make distclean
            rm -rf dist build .eggs
            rm -rf ~/.venv/labs

        </div>

    4.  Activate the virtual environment.

            [user@host rht-labs-core]$ cd ..
            [user@host ~]$ source ~/.venv/labs/bin/activate
            (labs) [user@host ~]$

    5.  There are two PyPi servers: development and production. Select
        the appropriate for your environment.

        - Development:
          <https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple/>

        - Production:
          <https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/simple/>

        <!-- -->

            (labs) [user@host ~]$ export PIP_EXTRA_INDEX_URL=https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple/

    6.  Verify that the `pip3` version used is inside the virtual
        environment.

    <!-- -->

        (labs) [user@host ~]$ which pip3
        ~/.venv/labs/bin/pip3

2.  Install the example package `rht-labs-gl006` as an editable copy
    from the source directory

        (labs) [user@host ~]$ pip3 install --editable rht-labs-core/packages-gl006
        Looking in indexes: https://pypi.org/simple, https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple/
        Obtaining file:///home/user/rht-labs-core/packages-gl006
          Preparing metadata (setup.py) ... done
        Collecting rht-labs-core~=2.5.0
          Downloading https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/packages/rht-labs-core/2.5.0/rht-labs-core-2.5.0.tar.gz (22 kB)
          Preparing metadata (setup.py) ... done
        Collecting rht-labs-ocp~=0.2.0
          Downloading https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/packages/rht-labs-ocp/0.2.0/rht-labs-ocp-0.2.0.tar.gz (15 kB)

        ...output omitted...

        Installing collected packages: rht-labs-ocp, rht-labs-core, rht-labs-gl006
            Running setup.py install for rht-labs-ocp ... done
            Running setup.py install for rht-labs-core ... done
          Running setup.py develop for rht-labs-gl006
        Successfully installed rht-labs-core-2.5.0 rht-labs-gl006-0.0.6 rht-labs-ocp-0.2.0

    1.  Ensure that the `lab` command is executed from the virtual
        environment.

    <!-- -->

        (labs) [user@host ~]$ which lab
        ~/.venv/labs/bin/lab

3.  Select the **GL006** lab to test your development environment.

        (labs) [user@host ~]$ lab select gl006

    1.  This creates or updates a development configuration file at
        `~/.grading/config.yaml`.

    ``` yaml
    rhtlab:
      course:
        sku: gl006
      logging:
        level: error
        path: /tmp/log/labs/
    ```

4.  Test your development environment by running the **GL006** start and
    finish functions.

        (labs) [user@host ~]$ lab start example-python
        ...output omitted...

        (labs) [user@host ~]$ lab finish example-python
        ...output omitted...

5.  As an example, test the **core** source code for good form by
    running the Python linter.

    1.  You will run the linter against your modules during development

    2.  The linter should not return any error or warning messages in
        this example

    <!-- -->

        (labs) [user@host ~]$ cd rht-labs-core/
        (labs) [user@host rht-labs-core]$ make lint
        python -m flake8

6.  As an example, run the test scripts for the **core** library.

    1.  You will write and run test scripts against your modules during
        development

        <div class="note">

        The output may show a different `platform` and `rootdir` when
        running in macOS.

        </div>

            (labs) [user@host rht-labs-core]$ make test
            python -m pytest -x
            ============================= test session starts ==============================
            platform linux -- Python 3.6.8, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
            rootdir: /home/user/rht-labs-core, configfile: pytest.ini
            collected 48 items

            tests/labs/environment_test.py .                                         [  2%]
            tests/unit/test_labconfig.py ..                                          [  6%]
            tests/unit/test_labload.py .                                             [  8%]
            tests/unit/test_lablog.py ........                                       [ 25%]
            tests/unit/test_userinterface.py ....                                    [ 33%]
            tests/unit/common/test_git.py ..........                                 [ 54%]
            tests/unit/common/test_tasks.py ..................                       [ 91%]
            tests/unit/common/test_workspace.py ....                                 [100%]

            ============================== 48 passed in 0.54s ==============================

    <div class="note">

    Linting and Testing are part of the Continuous Integration pipeline
    for the **core** library.

    </div>

7.  Deactivate your isolated Python environment session when you are
    finished developing.

        (labs) [user@host rht-labs-core]$ deactivate
        [user@host rht-labs-core]$

This concludes this guided exercise.

## Next Steps

The next training module will help you:

- Set up a new source folder

- Tell the lab framework about that source folder (dynamic loading)

- Code your first lab module (script)


