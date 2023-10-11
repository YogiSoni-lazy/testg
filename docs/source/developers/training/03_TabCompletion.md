# Using Tab Completion

## Concepts

After entering the `lab` command, you can hit the *tab* key twice at the
command line and you will be offered choices for what subcommands or
arguments are available in the context of your previous CLI state.

This is a feature of bash and is supported at least on macOS and Linux.

Tab completion depends upon executing a bash script called
`lab-completion.sh` within your active terminal shell. This can be
accomplished by either ensuring execution of the shell script via
`~/.bash_profile`, `~/.bashrc` (or equivalent), or by placing the script
in a special location called `bash_completion.d` where the shell will
load it on each login.

The following exercise assists you in getting tab completion installed
and guides you to use this feature of the `lab` CLI.

## Guided Exercise 3.1

### Prepare the environment

1.  Start your Python *virtual environment* if you haven’t activated it
    yet:

        [user@host ~]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ~]$

2.  Select the **GL006** course.

        (labs) [user@host ~]$ lab select gl006

3.  Ensure that bash *tab completion* support is installed in your OS.

    1.  In **RHEL** this is provided by the bash completion RPM.

            (labs) [user@host ~]$ sudo dnf -y install bash-completion

    2.  On **macOS** this installed with `brew`

    <!-- -->

        (labs) [user@host ~]$ brew install bash-completion

### Set up tab completion for `bash`

1.  Add a line to `~/.bashrc` to enable tab completion for all new shell
    windows:

2.  Save the tab completion code to a file and copy it to
    `bash_completion.d`

    1.  On **RHEL** this location is `/etc/bash_completion.d`

    2.  On **macOS** this location is
        `/usr/local/etc/bash_completion.d`.

<!-- -->

    (labs) [user@host ~]$ export COMPLETION_DIR="/etc/bash_completion.d"
    (labs) [user@host ~]$ lab completion bash > lab_completion.bash
    (labs) [user@host ~]$ sudo cp lab_completion.bash ${COMPLETION_DIR}/
    (labs) [user@host ~]$ rm lab_completion.bash
    (labs) [user@host ~]$ ls ${COMPLETION_DIR}/lab_completion.bash
    /etc/bash_completion.d/lab_completion.bash

### Test tab completion in a new *shell*

1.  Test tab completion for the `lab` command.

    1.  Open a new terminal window, that will `source` the tab
        completion logic into the new shell.

    2.  Activate the Python virtual environment and check if the lab
        command is recognized

    <!-- -->

        [user@host ~]$ source ~/.venv/labs/bin/activate

        (labs) [user@host ~]$ which lab
        ~/.venv/labs/bin/lab

        (labs) [user@host ~]$ lab <tab><tab>
        completion  grade       select      upgrade
        finish      install     start

2.  Enter `lab st<tab>` and the command will be expanded to `lab start`.

3.  Ask for a list of lab scripts that are available:

        (labs) [user@host ~]$ lab start example-<tab><tab>
        example-autoplay   example-openshift  example-playbook   example-python

4.  Deactivate your isolated Python environment session when you are
    finished developing.

        (labs) [user@host ~]$ deactivate
        [user@host ~]$

This concludes this guided exercise.

## Next Steps

The next training module will help you understand the syntax and
implementation of the `lab` CLI command.

