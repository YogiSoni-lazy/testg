# Implementing Python lab scripts

## Concepts

Each lab script has the following general structure:

1.  Python imports.

2.  Python class definition.

3.  Class functions to implement verbs and actions.

Each component is described in detail:

1.  Python module
    [*docstring*](https://www.python.org/dev/peps/pep-0257/) that
    describes the course and guided exercise name, and a brief sentence
    of what operations are performed in the lab script:

    ``` python
    """
    Grading module for GL007 Guided Exercise 2.

    This module implements the start, grading, and finish actions.
    """
    ```

2.  Python `import` statements for libraries.

    ``` python
    import os
    import time
    ```

3.  Python `import` statements for `labs` components.

    ``` python
    from labs.grading import Default
    from labs.common import labtools, userinterface
    ```

4.  List of `_targets` (hosts) that this lab script should consider.

    ``` python
    _targets = [
        "localhost",
        # ...
    ]
    ```

5.  Python `class` definition, *docstring* and `LAB` identifier for the
    lab script.

    ``` python
    class ExercisePython(Default):
        """
        This is the DocString for the ExercisePython class
        """
        __LAB__ = "exercise-python"
    ```

6.  Methods to handle the `start()`, `grade()`, and `finish()` verbs.

    1.  The methods should be indented at the *class* level.

    2.  Each method defines an array of `items`.

        1.  Each item in the array has the following fields.

        |          |                                                                                                                                                     |
        |----------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
        | `label`  | Short, one line description of the **task**. It will be displayed to the student when running the lab script.                                       |
        | `task`   | Function to be called to execute the **task**.                                                                                                      |
        | `failed` | Boolean value that indicate either *success* (`False`) or *failure* (`True`) of the **task**.                                                       |
        | `fatal`  | Setting this attribute to `True` indicates that the lab script will exit if this **task** is not successful (`failed` is set to `True`).            |
        | `msgs`   | List of error messages that can be set by the **task** function when it fails. They are displayed to the student to provide additional information. |

    ``` python
        def start(self):
            items = [
                {
                    "label": "Checking lab systems",
                    "task": labtools.check_host_reachable,
                    "hosts": _targets,
                    "fatal": True,
                },
                {
                    "label": "Task that succeeds",
                    "task": self._start_sample_success_task,
                },
                {
                    "label": "Task that fails",
                    "task": self._start_sample_failure_task,
                },
                # ...
            ]
            userinterface.Console(items).run_items(action="Starting")

        def grade(self):
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
                # ...
            ]
            ui = userinterface.Console(items)
            ui.run_items(action="Grading")
            ui.report_grade()

        def finish(self):
            items = [
                {
                    "label": "Checking lab systems",
                    "task": labtools.check_host_reachable,
                    "hosts": _targets,
                    "fatal": True,
                },
                {
                    "label": "Remove student's working directory",
                    "task": self._finish_workdir,
                },
                # ...
            ]
            userinterface.Console(items).run_items(action="Finishing")
    ```

7.  The first task the `start()`, `grade()`, and `finish()` handlers
    should perform is to invoke `labtools.check_host_reachable`. It
    checks that all hosts defined in the `_targets` list respond on port
    `22` to ensure **SSH** connectivity.

    ``` python
    _targets = [
        "localhost",
        # ...
    ]

    class ExercisePython(Default):

        # ...

        def start(self):
            items = [
                {
                    "label": "Checking lab systems",
                    "task": labtools.check_host_reachable,
                    "hosts": _targets,
                    "fatal": True,
                },
                # ...
            ]
            # ...
    ```

8.  Each lab script define a set of functions to implement the
    `_start*`, `_grade*` and `_finish*` actions.

    1.  The functions should be indented at the *class* level.

    2.  Each function receives the `self` and `item` parameters.

        1.  The `item` parameter has the `label`, `task`, `failed`, and
            `msgs` components as described in the `start()`, `grade()`,
            and `finish()` methods.

    3.  Each function has the necessary Python code to perform a task
        and check wether it was successful or not.

        1.  Exception handing should be performed in each task function,
            unhandled exceptions will be raised to upper levels and will
            cause program termination.

    ``` python
        def _start_sample_success_task(self, item):
            item["failed"] = False
            time.sleep(1)

        def _start_sample_failure_task(self, item):
            item["failed"] = True
            item["msgs"] = [
                {"text": "Sample explanation of failure"},
                {"text": "Further explanation would go here"},
            ]
            time.sleep(1)
    ```

9.  **Lab watch**. Lab scripts can use the `labs.watch` API to watch a
    lab’s progress. When the `Console.watch_lab` method is used, the lab
    script keeps running, continuously executing a series of checks,
    which we call **lab watch steps**, until all checks pass.

``` python
class ExercisePython(Default):

    ...

    def start(self):

        ...

        watch_items = [
            check_file_exists,
            check_host_reachable,
        ]

        console = Console(
            items,
            watch_items
        )

        console.run_items(action="Starting")

        console.watch_lab(finish=self.finish)
```

1.  You must define watch step functions by using the `@watchstep`
    decorator, like the following example shows:

``` python
from labs.watch import watchstep, expect

...

@watchstep("File example.yaml must exist")
def check_file_exists():
    expect(
        os.path.exists("./example.yaml"),
        error="example.yaml does not exist",
        hints=["You might want to create the file"]
    )
```

1.  To verify whether or not a watch step is successful, you must call
    the `expect` function, and pass a boolean value. Optionally, you can
    pass an error message and a list of hint messages in case the check
    does not pass.

2.  You can also use the `finish` parameter of the `Console.watch_lab`
    function to call the lab `finish` method after all watch steps pass.
    The `action` parameter is also optional. If not provided, the script
    prints `Watching lab…​`.

``` python
console.watch_lab(
    checks=[check_1, check_2],
    action="Watching lab ABC...",
    finish=self.finish
)
```

## Guided Exercise 6.1

1.  Start your Python *virtual environment* if you haven’t activated it
    yet:

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
        path: /tmp/log/labs
    ```

3.  Copy the exercise file

    1.  Copy the example file `exercise-python.py` to
        `rht-labs-gl007/src/gl007/`:

    <!-- -->

        (labs) [user@host ~]$ cp rht-labs-core/docs/training/files/exercise-python/exercise-python.py rht-labs-gl007/src/gl007/
        (labs) [user@host ~]$ ls rht-labs-gl007/src/gl007/exercise-python.py
        rht-labs-gl007/src/gl007/exercise-python.py

4.  Execute the `start` routine

    1.  Start the `exercise-python` lab script and notice the following:

        1.  Most tasks show a `SUCCESS` status.

        2.  Two tasks are marked as `FAIL`.

        3.  One of the *failed* tasks show extra information about the
            failure.

            <div class="note">

            All tasks should have a `SUCCESS` status when running the
            `start`, `grade`, and `finish` functions. The errors shown
            here are for demonstration purposes only.

            </div>

        <!-- -->

            (labs) [user@host ~]$ lab start exercise-python

            Starting lab.

             · Checking lab systems .............................................. SUCCESS
             · Create a test file ................................................ SUCCESS
             · Task that succeeds ................................................ SUCCESS
             · Task that fails ................................................... FAIL
                - Sample explanation of failure
                - Further explanation would go here
             · Do nothing task that always succeeds .............................. SUCCESS
             · Do nothing task that always fails ................................. FAIL

    2.  Open the `exercise-python.py` script and go to the definition of
        `_start_sample_success_task` and `_start_sample_failure_task`
        functions.

            (labs) [user@host ~]$ view ~/rht-labs-gl007/src/gl007/exercise-python.py

        1.  Notice how the task marked with `SUCCESS` assigns
            `item["failed"]` to `False` and the one marked as `FAIL` one
            assigns `True` to reflect the status.

        2.  Also check the use and structure of `item["msgs"]` to
            display further information to the student when a task
            fails.

            <div class="note">

            This is for demonstration purposes only. You should not do
            this when coding real lab scripts.

            </div>

        ``` python
            def _start_sample_success_task(self, item):
                item["failed"] = False
                time.sleep(1)

            def _start_sample_failure_task(self, item):
                item["failed"] = True
                item["msgs"] = [
                    {"text": "Sample explanation of failure"},
                    {"text": "Further explanation would go here"},
                ]
                time.sleep(1)
        ```

    3.  The `_start_conf_deployed` task creates a `ExercisePython`
        directory and a file.

            (labs) [user@host ~]$ tree ~/GL007/
            /home/user/GL007/
            └── ExercisePython
                └── test_file

    4.  The `_start_conf_deployed` task implements the logic to create a
        directory and a test file.

        1.  The `student_working_dir` will have the full path to
            `~/SKU/lab_name`.

        2.  It uses a wrapper function `labtools.mkdir` to create the
            directory.

        3.  It also creates the `test_file` with standard Python `open`
            and `write` functions.

            ``` python
                def _start_conf_deployed(self, item):
                    """
                    Create a sample file in ~/SKU/lab_name
                    """
                    lab_name = type(self).__name__
                    student_working_dir = os.path.join(
                        labtools.get_sku_path(),
                        lab_name
                    )

                    # Create the ~/SKU/lab_name directory with a wrapper function
                    mkdir_result = labtools.mkdir(student_working_dir)
                    if mkdir_result["failed"]:
                        item["failed"] = True
                        item["msgs"] = [{"text": "Directory could not be created"}]
                        return

                    # Create a test_file inside ~/SKU/lab_name with native Python code
                    file_path = os.path.join(
                        student_working_dir,
                        "test_file"
                    )
                    file_content = "Hello world!" + "\n"
                    try:
                        with open(file_path, 'w+') as file:
                            file.write(file_content)
                        item["failed"] = False
                    except Exception:
                        item["failed"] = True
                        item["msgs"] = [
                            {"text": "Can't write to file: {}".format(file_path)}
                        ]
                        return
            ```

        4.  The wrapper function for `labtools.mkdir` will return a
            dictionary. You can check the `failed` key to see if the
            directory creation was successful or not and set
            `item["failed"]` and `item["msgs"]` appropriately:

            ``` python
                    # Create the ~/SKU/lab_name directory with a wrapper function
                    mkdir_result = labtools.mkdir(student_working_dir)
                    if mkdir_result["failed"]:
                        item["failed"] = True
                        item["msgs"] = [{"text": "Directory could not be created"}]
                        return
            ```

        5.  The standard Python functions may throw exceptions and the
            developer should implement code to handle them:

        <div class="note">

        The broad exception handling is provided here for demonstration
        purposes only. It is advised to handle all the *particular*
        exceptions instead.

        </div>

    ``` python
            # Create a test_file inside ~/SKU/lab_name with native Python code
            file_path = os.path.join(
                student_working_dir,
                "test_file"
            )
            file_content = "Hello world!" + "\n"
            try:
                with open(file_path, 'w+') as file:
                    file.write(file_content)
                item["failed"] = False
            except Exception:
                item["failed"] = True
                item["msgs"] = [
                    {"text": "Can't write to file: {}".format(file_path)}
                ]
                return
    ```

5.  Execute the `grade` routine

    1.  The `grade` action will invoke the `_grade_test` function that
        checks if the `test_file` is in the `~/GL007/ExercisePython`
        directory.

        1.  The *overall lab grade* will be marked as `PASS` if **all**
            grading tasks report a `SUCCESS` status, it will return a
            `FAIL` status otherwise.

        <!-- -->

            (labs) [user@host ~]$ lab grade exercise-python

            Grading lab.

             · Checking lab systems .............................................. SUCCESS
             · Check test_file ................................................... SUCCESS

            Overall lab grade: PASS

    2.  The code structure is similar to the *start* functions.

        1.  This function uses standard Python code to perform the
            check.

        2.  It assigns `item["failed"] = True` if the `test_file` is not
            present under `GL007/ExercisePython`.

        ``` python
            def _grade_test(self, item):
                """
                Check if test_file exists on ~/SKU/lab_name
                """
                lab_name = type(self).__name__
                file_path = os.path.join(
                    labtools.get_sku_path(),
                    lab_name,
                    "test_file"
                )
                if not os.path.exists(file_path):
                    item["failed"] = True
                    item["msgs"] = [{"text": "File does not exist"}]
        ```

    3.  You can manually check if the file is on the desired location
        and check its contents:

    <!-- -->

        (labs) [user@host ~]$ ls ~/GL007/ExercisePython/test_file
        /home/user/GL007/ExercisePython/test_file

        (labs) [user@host ~]$ cat ~/GL007/ExercisePython/test_file
        Hello World!

6.  Test fail condition for the `grade` routine

    1.  Locate the `_grade_test` function in the `exercise-python.py`
        file.

        1.  Change the filename to check from `test_file` to
            `nonexistent_file` and save the file.

``` python
        file_path = os.path.join(
            labtools.get_sku_path(),
            lab_name,
            "nonexistent_file"
        )
```

1.  Run the `lab grade exercise-python` command again and expect it to
    fail since it will not find the desired file.

        (labs) [user@host ~]$ lab grade exercise-python

        Grading lab.

         · Checking lab systems .............................................. SUCCESS
         · Check test_file ................................................... FAIL
            - File does not exist

        Overall lab grade: FAIL

2.  Undo your changes and save the file again to restore the working
    behavior.

    1.  Execute the `finish` routine

        1.  When running the `finish` action, the cleanup function
            `_finish_workdir` is called.

        <!-- -->

            (labs) [user@host ~]$ lab finish exercise-python

            Finishing lab.

             · Checking lab systems .............................................. SUCCESS
             · Remove student's working directory ................................ SUCCESS

        1.  This function is executing the equivalent of
            `rm -rf ~/GL007/ExercisePython` using the `delete_workdir`
            function defined in the `labtools` library.

            There are some common tasks defined in the core `labtools`
            library functions.

        2.  After the `_finish_workdir` function is executed the
            ExercisePython directory is removed from `~/GL007/`.

    <!-- -->

        (labs) [user@host ~]$ tree ~/GL007/
        /home/user/GL007/

This concludes this guided exercise.

## Next Steps

### Ansible

If you are interested in running Ansible playbooks to perform lab tasks
and checks, review the next module.



### Python Tasks Module

The `labs.common` module includes common reusable functions and tasks.

- The `labs.common.tasks` module includes tasks to create and remove the
  common directories used in the lab scripts.

``` python
from labs.common import labtools
items = [
    {
        "label": "Copy exercise files",
        "task": labtools.copy_lab_files,
        "lab_name": self.__LAB__,
        "fatal": True,
    },
    {
        "label": "Remove lab files",
        "task": labtools.delete_workdir,
        "lab_name": self.__LAB__,
        "fatal": True
    },
]
```

- The `labs.common.tasks` module includes general-purpose tasks, which
  follow the standard task signature (`task(item: Dict)`) and are easily
  reusable. For example, you can use the `git` task as follows:

``` python
from labs.common import tasks

item = {
    "label": "Checkout main branch",
    "task": tasks.git,
    "command": ["checkout", "main"],
    "repopath": "/path/to/your/repo",
    "fatal": True,
}
```

- The `labs.common.workspace` configures the lab workspace and creates a
  working directory. Courses using this module should create its own
  config class, as a subclass of `ClassroomConfigFile` or
  `ClassroomConfigJsonFile`.

``` python
import os
from labs.common.config import ClassroomConfigJsonFile
from labs.common.workspace import Workspace

CONFIG_FILEPATH = os.environ.get("CONFIG_FILEPATH")

class DO400ClassroomConfig(ClassroomConfigJsonFile):

    ocp_api: str
    ocp_username: str
    ocp_password: str

    def __init__(self,
                 workdir: str,
                 ocp_api: str,
                 ocp_username: str,
                 ocp_password: str):

        self.ocp_api = ocp_api
        self.ocp_username = ocp_username
        self.ocp_password = ocp_password

        super().__init__(CONFIG_FILEPATH, workdir)


config = DO400ClassroomConfig(
    #...
)
workspace = Workspace().configure(config)
```

Find more examples in [DO400
scripts](https://github.com/RedHatTraining/DO400/tree/master/classroom/grading/do400).
