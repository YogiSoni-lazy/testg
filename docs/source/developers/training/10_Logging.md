# Using the Logging Framework

## Prerequisites

You must complete at least the next guided exercises before proceeding
with this exercise.

1.  [Guided Exercise 1.1: **Establishing the Development
    Environment**](01_DevelopmentEnvironment.adoc)

2.  [Guided Exercise 6.1: **Implementing Python lab
    scripts**](06_PythonLabScript.adoc)

## Concepts

In this exercise, you will learn how to make use of the logging
functions in a lab script.

### Configuration file

The configuration for the `lab` command is stored in the
`~/.grading/config.yaml` file.

``` yaml
rhtlab:
  course:
    sku: gl007
  logging:
    level: info
    path: /tmp/log/labs/
```

Each field is described in the following table.

|           |                                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------------|
| `rhtlab`  | Contains the definition of the course version (`sku`) under the `course` option.                          |
| `logging` | Contains the definition of the log level and log path.                                                    |
| `level`   | Specifies the log level you want to retrieve. Messages with a lower level are not stored in the log file. |
| `path`    | Provides the log directory. This can be changed according to your configuration.                          |

You can adjust the **log level** and the **log path**.

### Log level

In the **Establishing the Development Environment** guided exercise, you
created a Python *virtual environment*, and a development configuration
file with the default values for the `logging` section.

The supported log levels are described in the following table.

|            |                                                                                                                                                        |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `critical` | This messages appear when a really serious problem occurs during the execution of development script, even causing the entire script fail to continue. |
| `error`    | It is produced in the execution of your development script. It appears when the execution wasn’t able to perform an action.                            |
| `warning`  | The warnings alerts usually appear before an error happens by way of prevention.                                                                       |
| `info`     | It is used to indicate that functions were executed correctly.                                                                                         |
| `debug`    | This logs collects detailed information when diagnosing problems.                                                                                      |

### Log path

The `~/.grading/config.yaml` file has a field that allows you to specify
the file or directory where the logs will be saved.

- If the destination is a **file**, the logs for all lab scripts will be
  saved there.

- If the location is a **directory** (path ending with `/`), every lab
  script will save its logs to a different file (e.g.
  `/tmp/log/labs/example-logging`, and `/tmp/log/labs/example-python`).

The destination files and directories will be created if they don’t
exist.

## Guided Exercise 10.1

1.  Start your Python *virtual environment* if you haven’t activated it
    yet.

        [user@host ~]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ~]$

2.  Select the **GL007** course.

        (labs) [user@host ~]$ lab select gl007

    1.  Be sure to have **GL007** activated in the
        `~/.grading/config.yaml` file.

    ``` yaml
    rhtlab:
      course:
        sku: gl007
      logging:
        level: error
        path: /tmp/log/labs/
    ```

3.  Inside the `rht-labs-gl007/src/gl007` directory create a copy of the
    `exercise-python.py` and name it `exercise-logging.py`.

        (labs) [user@host ~]$ cp rht-labs-core/docs/training/files/exercise-python/exercise-python.py rht-labs-gl007/src/gl007/exercise-logging.py

4.  Edit the `exercise-logging.py` script to call the log library.

    1.  Open the file `~/rht-labs-gl007/src/gl007/exercise-logging.py`.

            (labs) [user@host ~]$ vim ~/rht-labs-gl007/src/gl007/exercise-logging.py

    2.  Add an import for the Python logging library.

        ``` python
        import os
        import time
        import logging
        ```

    3.  Change the class name, *docstring* and `__LAB__` value.

        ``` python
        class ExerciseLogging(Default):
            """
            This is the DocString for the ExerciseLogging class
            """
            __LAB__ = "exercise-logging"
        ```

    4.  Start the lab script to verify that its working correctly.

        <div class="note">

        The two tasks marked as `FAIL` are for demonstration purposes.
        You can safely ignore them.

        </div>

            (labs) [user@host ~]$ lab start exercise-logging

            Starting lab.

             · Checking lab systems .............................................. SUCCESS
             · Create a test file ................................................ SUCCESS
             · Task that succeeds ................................................ SUCCESS
             · Task that fails ................................................... FAIL
                - Sample explanation of failure
                - Further explanation would go here
             · Do nothing task that always succeeds .............................. SUCCESS
             · Do nothing task that always fails ................................. FAIL

    5.  Locate the `grade` function definition and call the
        `logging library` to print *debug* and *warning* messages. This
        will collect the logs associated with the lab script execution
        in the `/tmp/log/labs/exercise-logging` file.

        ``` python
            def grade(self):
                """
                Perform evaluation steps on the system
                """
                logging.debug("Entering 'grade' function")
                items = [
                    {
                        "label": "Checking lab systems",
                        "task": labtools.check_host_reachable,
                        "hosts": _targets,
                        "fatal": True,
                    },
                    {
                        "label": "Check test_file",
                        "task": self._grade_test,
                    },
                ]
                if not items:
                    logging.warning("'items' array is empty!")
                logging.debug("At 'grade' function, before 'ui'")
                ui = userinterface.Console(items)
                logging.debug("At 'grade' function, before 'run_items'")
                ui.run_items(action="Grading")
                logging.debug("At 'grade' function, before 'report_grade'")
                ui.report_grade()
                logging.debug("Leaving 'grade' function")
        ```

    6.  Now locate the `_grade_test` function and add a few more
        `logging` statements.

        ``` python
            def _grade_test(self, item):
                """
                Check if test_file exists on ~/SKU/lab_name
                """
                logging.debug("Entering '_grade_test' function")
                lab_name = type(self).__name__
                logging.info("lab_name = %s", lab_name)
                file_path = os.path.join(
                    labtools.get_sku_path(),
                    lab_name,
                    "test_file"
                )
                logging.info("file_path = %s", file_path)
                if not os.path.exists(file_path):
                    item["failed"] = True
                    item["msgs"] = [{"text": "File does not exist"}]
                    logging.error(item["msgs"])
                logging.debug("Leaving '_grade_test' function")
        ```

    7.  Execute the grade function for `exercise-logging`.

            (labs) [user@host ~]$ lab grade exercise-logging

            Grading lab.

             · Checking lab systems .............................................. SUCCESS
             · Check test_file ................................................... SUCCESS

            Overall lab grade: PASS

        1.  Check that the log file was created.

    <!-- -->

        (labs) $ tree /tmp/log
        /tmp/log
        └── labs
            └── exercise-logging

5.  Check the file at `/tmp/log/labs/exercise-logging` to verify the
    written logs. You should something similar to the next lines.

        (labs) [user@host ~]$ tail /tmp/log/labs/exercise-logging
        2021-02-25 17:53:05,669:exercise-logging:INFO:lablog.py(200)                #################### exercise-logging ####################
        2021-02-25 17:53:06,672:exercise-logging:INFO:exercise-logging.py(167)                lab_name = ExerciseLogging
        2021-02-25 17:53:06,672:exercise-logging:INFO:exercise-logging.py(173)                file_path = /home/user/GL007/ExerciseLogging/test_file

As you can see, there are not `debug` logs stored in the file, and it’s
because the assigned `info` log level has a greater priority.

<div class="note">

If you get any problem, you can check the `exercise-logging.py` solution
file in the `~/rht-labs-core/docs/training/files/exercise-logging`
directory.

</div>

This concludes this guided exercise.

## Next Steps

This module concludes the training path. If you have any question, want
to open a new issue or you to review the sprint course, go check out the
next links.

1.  [Github
    issues](https://github.com/RedHatTraining/rht-labs-core/issues)

2.  [Zenhub
    board](https://app.zenhub.com/workspaces/dynolabs-team-5fbba73313d49000167afd23/board)

3.  [DynoLabs chat
    room](https://mail.google.com/chat/u/0/#chat/space/AAAA6DP4-qg)
