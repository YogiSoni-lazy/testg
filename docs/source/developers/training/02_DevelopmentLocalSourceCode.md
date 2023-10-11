# Working with Local Source Code

## Prerequisites

You must complete Guided Exercise 1.1 before proceeding with this
exercise.

## Concepts

In the previous module you used `pip3` to install the `rht-labs-core`,
`rht-labs-ocp`, and `rht-labs-gl006` packages in the *editable* format.
This means that your changes to the source code will be reflected
immediately the next time you execute the `lab` command without having
to package and upload to the PyPI server.

In the following guided exercise, you will create the source directory
for **GL007**, your practice course. You will also create a
`Hello World!` example for your first lab module (script).

## Guided Exercise 2.1

1.  Start your Python *virtual environment* if you haven’t activated it
    yet:

        [user@host ~]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ~]$

2.  Create a new source tree for the **GL007** practice course outside
    of the `rht-labs-core` directory structure.

    1.  Create the `~/rht-labs-gl007` directory. Within the
        `rht-labs-gl007` directory, create the `src/gl007` directories.

            (labs) [user@host ~]$ mkdir -vp ~/rht-labs-gl007/src/gl007
            mkdir: created directory '/home/user/rht-labs-gl007'
            mkdir: created directory '/home/user/rht-labs-gl007/src'
            mkdir: created directory '/home/user/rht-labs-gl007/src/gl007'

        <div class="important">

        Do not create the `~/rht-labs-gl007` directory within the
        `~/rht-labs-core` directory structure.

        </div>

    2.  Make the `gl007` directory a Python module by creating the
        `__init__.py` file. Copy the
        `~/rht-labs-core/packages-gl006/src/gl006/__init__.py` file as
        an example.

            (labs) [user@host ~]$ cp ~/rht-labs-core/packages-gl006/src/gl006/__init__.py \
              ~/rht-labs-gl007/src/gl007/

    3.  Modify the
        `~/rht-labs-core/packages-gl006/src/gl007/__init__.py` file to
        change `gl006` to `gl007`. The resulting file has the following
        content. This code helps the `lab` command find Ansible roles
        for the **GL007** course.

            (labs) [user@host ~]$ sed -i 's/gl006/gl007/g' ~/rht-labs-gl007/src/gl007/__init__.py

    ``` yaml
    import os
    import importlib
    try:
        module = importlib.import_module("*gl007*")
        \\__ANSIBLE_ROLES_PATH__ =\
            os.path.dirname(module.\\__file__) + "/ansible/roles"
    except ModuleNotFoundError:
        pass
    ```

3.  Copy the `setup.cfg` and `setup.py` files to the `~/rht-labs-gl007/`
    directory.

        (labs) [user@host ~]$ cp ~/rht-labs-core/docs/training/files/exercise-source/setup.* \
          ~/rht-labs-gl007/

4.  Copy the `version.py` file to the `~/rht-labs-gl007/src/gl007/`
    directory.

        (labs) [user@host ~]$ cp ~/rht-labs-core/docs/training/files/exercise-source/src/gl007/version.py \
          ~/rht-labs-gl007/src/gl007/

5.  Verify the contents of your `rht-labs-gl007` source directory.

        (labs) [user@host ~]$ tree ~/rht-labs-gl007
        rht-labs-gl007
        ├── setup.cfg
        ├── setup.py
        └── src
            └── gl007
                ├── __init__.py
                └── version.py

6.  Install your new course as a development package.

        (labs) [user@host ~]$ pip install --editable ~/rht-labs-gl007
        Looking in indexes: https://pypi.org/simple, https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple/
        Obtaining file:///home/user/rht-labs-gl007
        ...output omitted...
        Installing collected packages: rht-labs-gl007
          Running setup.py develop for rht-labs-gl007
        Successfully installed rht-labs-gl007-0.0.1

7.  Create your first lab module (script).

    1.  Use the `lab` command to select the **GL007** course

            (labs) [user@host ~]$ lab select gl007

    2.  Try to start the lab script with the empty `rht-labs-gl007`
        Python package you just installed. Notice the warning message
        from the core library.

            (labs) [user@host ~]$ lab start exercise-source
            Script exercise-source not in course library gl007

    3.  Add an empty Python script called `exercise-source.py` to the
        `src/gl007` directory and open it in a text editor.

            (labs) [user@host ~]$ cd rht-labs-gl007
            (labs) [user@host rht-labs-gl007]$ touch src/gl007/exercise-source.py

    4.  Import the `Default` grading class.

    5.  Create the `ExerciseSource` class that uses the `Default` class
        as a base.

    6.  Define the lab name in the `__LAB__` variable.

    7.  Create a `start` function that just prints a message on the
        screen.

    ``` python
    from labs.grading import Default


    class ExerciseSource(Default):
        __LAB__ = "exercise-source"

        def start(self):
            print("Hello World!")
    ```

8.  Test the new course.

    1.  Check that the `sku: gl007` line is present in the
        `~/.grading/config.yaml` file.

        ``` yaml
        rhtlab:
          course:
            sku: gl007
          logging:
            level: error
            path: /tmp/log/labs/
        ```

    2.  Execute the start for `exercise-source`. You should see a
        message printed on the screen.

    <!-- -->

        (labs) [user@host rht-labs-gl007]$ lab start exercise-source
        Hello World!

9.  Define the `finish` function

    ``` python
    from labs.grading import Default


    class ExerciseSource(Default):
        __LAB__ = "exercise-source"

        def start(self):
            print("Hello World!")

        def finish(self):
            print("This is the finish function from '{}'".format(self.__LAB__))
    ```

    1.  Run the `grade` function and notice the message that is printed
        on the screen. This happens because there is no `grade` function
        defined for this lab script.

            (labs) [user@host rht-labs-gl007]$ lab grade exercise-source
            The grade command is not supported for this lab.

    2.  Run the `finish` function for the lab script. This time the
        defined function is executed and another message is printed on
        the screen.

    <!-- -->

        (labs) [user@host rht-labs-gl007]$ lab finish exercise-source
        This is the finish function from 'exercise-source'

<div class="note">

The complete **GL007** module directory used for this exercise is
located at: `~/rht-labs-core/docs/training/files/exercise-source`

</div>

1.  Deactivate your isolated Python environment session when you are
    finished developing.

        (labs) [user@host rht-labs-gl007]$ cd
        (labs) [user@host ~]$ deactivate
        [user@host ~]$

This concludes this guided exercise.

## Next Steps

The next training module will help you configure and use tab completion
for the `lab` CLI command.


