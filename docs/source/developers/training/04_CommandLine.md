# Using the Command Line

## Concepts

The command line interface (CLI) consists of a single `lab` command. The
CLI has numerous functions including:

- Getting help, or a list of options

- Loading a new course library (package)

- Executing a verb (start, grade, finish) against a lab module (script)

- Get the version of the lab framework

### The `select` command

This command activates a course package. You can use it in order to be
able to start the lab scripts for a given course.

1.  Activate the Python virtual environment.

        [user@host ~]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ~]$

    1.  Select the **GL006** course to use its lab scripts (you can use
        tab-completion for the verbs and exercises)

            (labs) [user@host ~]$ lab select gl006
            (labs) [user@host ~]$ lab start example-<tab><tab>
            example-autoplay   example-openshift  example-playbook   example-python

    2.  Select the **GL007** course to use its lab scripts

    <!-- -->

        (labs) [user@host ~]$ lab select gl007
        (labs) [user@host ~]$ lab start exercise-source

In the following guided exercise, you will play with the command line.

## Guided Exercise 4.1

1.  Start your Python *virtual environment* if you haven’t activated it
    yet:

        [user@host ~]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ~]$

2.  Select the **GL006** course.

        (labs) [user@host ~]$ lab select gl006

3.  Make sure your lab environment is configured for course **GL006** in
    the `~/.grading/config.yaml` file.

    ``` yaml
    rhtlab:
      course:
        sku: gl006
      logging:
        level: error
        path: /tmp/log/labs/
    ```

4.  Get a list of commands that are available from the CLI

        (labs) [user@host ~]$ lab --help
        Usage: lab [OPTIONS] COMMAND [ARGS]...

          CLI for Red Hat Training lab grading.

        Options:
          -v, --version  Get lab framework version number and exit.
          --help         Show this message and exit.

        Commands:
          completion  Print completion commands for a given shell
          finish      Finish the lab session.
          grade       Grade the lab.
          install     Install the course library.
          select      Select the active course grading library.
          start       Start the lab session.
          upgrade     Upgrade the course library.

5.  Get the version of the framework.

        (labs) [user@host ~]$ lab --version
        Lab framework version 2.5.0

    <div class="note">

    Your lab framework version might be different.

    </div>

6.  Get the options for the `start` command:

        (labs) [user@host ~]$ lab start --help
        Usage: lab start [OPTIONS] SCRIPT

          Start the lab session.

          SCRIPT is the name of the lab script. This variable supports tab
          completion.

        Options:
          --help  Show this message and exit.

    <div class="note">

    You can get help for any command by appending `--help`.

    </div>

7.  Get help for the `select` command.

        (labs) [user@host ~]$ lab select --help
        Usage: lab select [OPTIONS] SKU

          Select the active course grading library.

          SKU is the course code, such as gl006

        Options:
          -f, --force  Set course library even if it is not installed (mainly for
                       course developers).

          --help       Show this message and exit.

This concludes this guided exercise.

In the following guided exercise, you will review the CLI code base to
identify key features of the lab framework.

## Guided Exercise 4.2

1.  Open `~/rht-labs-core/src/labs/lab.py` in your favorite editor.

2.  Find the core function for the CLI:

    ``` python
    @click.group(name='lab', invoke_without_command=True)
    @click.pass_context
    @click.option('--version', '-v', is_flag=True,
                  help='Get lab framework version number and exit.')
    def main(ctx, version):
    ```

3.  Optionally, explore the `click` library documentation at
    [click](https://click.palletsprojects.com/en/7.x/).

4.  Identify the functions (`def`) for each of the lab commands:
    `select`, `start`, `grade`, and `finish`. Notice the `click`
    *decorators* for each function.

5.  Open the `src/labs/labload.py` file and check the implementation of
    the `import_grading_library` function.

    1.  Note how the lab module (script) is loaded dynamically:

        ``` python
        def import_grading_library(config, name):
            cache = loadcache()
            course = labconfig.get_course_sku()
            if name not in cache.keys():
                raise LabError("Script %s not in course library %s" % (name, course))
            cache_entry = cache[name]
            try:
                lablog_init(config, cache_entry["module"])
                module = importlib.import_module(course + "." + cache_entry["module"])
                class_ = getattr(module, cache_entry["class"])
                return class_()
            except ModuleNotFoundError:
                raise LabError("Script %s in course library %s or one of its "
                               "components was not found."
                               % (name, course))
        ```

    <div class="note">

    You can see in this code snippet that the script name passed on the
    command line must match a Python script file of the same name. Tab
    completion makes this easier for the student.

    </div>

6.  Deactivate your isolated Python environment session when you are
    finished developing.

        (labs) [user@host ~]$ deactivate
        [user@host ~]$

This concludes this guided exercise.

## Next Steps

The next training module will show you how to package your course for
distribution.

