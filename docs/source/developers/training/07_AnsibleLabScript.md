# Developing Exercises Using Ansible

Developers who are more familiar with Ansible than python can write
Ansible playbooks and run the playbooks from their lab scripts.

<div class="important">

The lab grading framework primarily focuses on courses that run on RHEL
systems, but it also includes courses that use Bring Your Own Device
(BYOD). **Do not** use Ansible for BYOD courses. Although Ansible
playbooks can target Windows machines, Windows machines cannot run
Ansible playbooks.

- <https://docs.ansible.com/ansible/latest/user_guide/windows_faq.html#can-ansible-run-on-windows>

</div>

## Reusability

Develop your Ansible code with the intention that you or someone else
can reuse it. Frequently, students perform one version of a task in a
guided exercise and a similar version of the task in a lab or
comprehensive review. Ideally, the playbooks, roles, or tasks files that
you created for one exercise can adapt to multiple variations, rather
than requiring a developer to create separate versions for each
exercise.

## Roles

Ansible roles provide an easy way to share functionality. Use the
`ansible-galaxy` command to create the skeleton directory structure for
a new role. Create roles for a course within the `ansible/roles/`
directory for the course package.

Set variables in either the `defaults/main.yml` or `vars/main.yml`
files. Remember that inventory variables override variables with the
same name in `defaults/main.yml`, but not in `vars/main.yml`. Playbook
variables with the same name take precedence over both of these variable
files.

Make it easy for developers to use your role by deleting any unused
files or directories within the file directory structure for your role.

Additionally, if a role that you create is really worth reusing, take
the time to complete the `README.md` and `meta/main.yml` files.

## Be flexible

Your team will be composed of developers with varying degrees of
proficiency in Ansible. Just as there are multiple ways to accomplish
tasks in Linux, there are multiple ways to write an Ansible playbook to
accomplish a task.

Developers less proficient in Ansible should be open to refactoring
their playbooks based on feedback from developers more proficient in
Ansible. Developers more proficient in Ansible should be open to
playbooks being created in a different way from how they would do it.

Deadlines will continue to limit the amount of time that developers can
spend creating and refining lab scripts and playbooks. With this in
mind, you might ask the following questions when performing a peer
review of a playbook:

- **Does the playbook work?**

  At a basic level, the playbook needs to work. It might not be pretty,
  reusable, or efficient, but it might be sufficient as long as it
  works.

- **Can the playbook be reused?**

  Ideally, a playbook can be reused for more than one exercise. This
  prevents having to copy the playbook if a lab or comprehensive review
  must perform similar actions.

  In general, a playbook should avoid hard coding values that might be
  different between exercises. Use variables rather than hard coding
  values. Variables can be defined in a playbook or in a separate file.
  They can be defined for a specific machine or a group of machines in
  either the `host_vars` or `group_vars` directories. They can be passed
  to the `ansible-playbook` command from the command line.

  <div class="note">

  Your python script has the ability to pass variables to your playbook
  in the same way that you pass variables to the `ansible-playbook`
  command.

  </div>

  If it makes sense, consider adding default values for variables. When
  using roles, default values for variables can be defined in either
  `defaults/main.yml` or `vars/main.yml`. An inventory variable with the
  same name takes precedence over `defaults/main.yml`, but does not take
  precedence over `vars/main.yml`.

  Jinja2 can provide default variable values. For example, default to
  using `/bin/bash` for the shell if `item['shell']` is not defined.

  ``` yaml
  shell: "{{ item['shell'] | default('/bin/bash') }}"
  ```

  You can omit a variable if it is not defined. For example, the Ansible
  `user` module does not require a value for the `comment` option. If
  `item['comment']` is not defined, then provide a null value.

  ``` yaml
  comment: "{{ item['comment'] | default(omit) }}"
  ```

  Be aware that developers can have different opinions on how to make a
  playbook reusable (or more reusable). This can include refactoring a
  playbook so that it becomes one or more roles. A playbook could be
  broken up into multiple task files. A playbook can use tags or a
  variable to define the actions that are run.

  Teams might come to an agreement on the preferred approach for
  reusability at the start of a project. Keep in mind that based on time
  constraints, having reusable code is less important than having
  playbooks that work.

- **Can the playbook be optimized or simplified?**

  Developers more proficient in Ansible can frequently find ways to
  optimize or simplify Ansible code. In some cases, the changes are a
  matter of personal preference. When making or suggesting changes, you
  might explain why the change is better. These explanations can help
  other developers become more proficient.

  The switch to the new lab grading framework will have some growing
  pains. Playbooks will not be perfect for the first round of classes,
  but they should improve as developers start using playbooks to develop
  exercises.

## Fail fast

Many tasks use a `when` conditional to decide if the task should be run
or skipped. For example, only run a task if a variable is defined or a
variable matches a specific value.

For variables that must be defined in order to run a playbook
successfully, consider adding one or more tasks using the `fail` module
at the top of your play. This can prevent false positives where a
playbook completes without any errors, but actually skips all tasks.

## Ansible directory skeleton

As developers implement the lab grading framework for real courses, a
skeleton version of the Ansible directory structure will emerge. At a
minimum, the skeleton should contain the following.

``` bash
ansible/
├── ansible.cfg
├── group_vars
├── host_vars
├── inventory
└── roles
```

This example uses an `inventory/` directory that contains a `hosts` file
and the `host_vars` and `group_vars` directories.

``` bash
ansible/
├── ansible.cfg
├── inventory
│   ├── group_vars
│   ├── hosts
│   └── host_vars
└── roles
```

- `ansible/ansible.cfg`

  The lab grading framework uses the `ansible/ansible.cfg` file by
  setting the ANSIBLE_CONFIG environment variable. For development and
  testing, avoid copying the `ansible.cfg` file to each exercise
  directory. You can either run your playbooks from the main `ansible/`
  directory, or you can set the `ANSIBLE_CONFIG` environment variable to
  provide an absolute path to the `ansible/ansible.cfg` file.

  The following shows a simple `ansible.cfg` file. Your team will likely
  make additional customizations.

      [defaults]
      inventory = ./inventory
      gathering = False

  Best practices indicate that you should not enable privilege
  escalation by default. Use `become: True` for plays or tasks that
  require privilege escalation.

  Gathering facts for each play can significantly increase the amount of
  time needed for a playbook to finish. Consider turning off fact
  gathering by default. You can always enable fact gathering for a
  specific play using `gather_facts: True` or by explicitly having a
  task that runs the `setup` module. If fact gathering is required, you
  might experiment with using the `gather_subset` option to only gather
  specific facts, such as the minimum facts (`min`) or hardware facts
  (`hardware`).

- `ansible/inventory`

  Using a single `ansible.cfg` file also eliminates the need to have
  multiple copies of inventory files. The inventory can be specified as
  a file, such as `ansible/inventory`, or as a directory, such as
  `ansible/inventory/`.

  As more exercise directories are added to the main `ansible/`
  directory, having a dedicated `ansible/inventory/` directory might
  make the main `ansible/` directory less cluttered.

  Delete the `host_vars` or `group_vars` directories if they are not
  used.

  The following shows a simple `ansible/inventory` or
  `ansible/inventory/hosts` file. Your team will specify all of the
  hosts available in your classroom environment. The hosts might be
  placed into one or more groups.

      localhost ansible_connection=local

- `ansible/roles/`

  The lab grading framework dynamically finds possible locations for
  Ansible roles. Your classroom environment might have core roles
  installed from `rht-labs-core`, technology roles installed from
  something such as `rht-labs-ocp`, and your course roles installed in
  `ansible/roles/`.

- `ansible/{files,tasks,templates,vars}`

  In addition to the exercise directories created within the main
  `ansible/` directory, your team might create directories for
  additional shared resources. These directories are optional.

# Developing Exercises Using Ansible Playbooks and Roles

In this exercise, you will create a python script that executes two
Ansible playbooks. One of the Ansible playbooks will use a new role that
you create.

This exercise assumes that you completed the first two training modules.
You created a virtual environment in the
`01_DevelopmentEnvironment.adoc` training module. You created the
**GL007** course in the `02_DevelopmentLocalSourceCode.adoc` training
module.

1.  Create a python script for a new exercise named `use-roles.py`.

    1.  Change into the `rht-labs-gl007/src/gl007/` course directory
        created in the second training module.

        ``` bash
        [user@host ~]$ cd ~/rht-labs-gl007/src/gl007/
        ```

    2.  Copy the
        `~/rht-labs-core/docs/training/files/module_07/examplePlaybook.py`
        script to a new file named `use-roles.py`.

        ``` bash
        [user@host gl007]$ cp ~/rht-labs-core/docs/training/files/module_07/examplePlaybook.py use-roles.py
        ```

        <div class="note">

        You will customize the python script later in the exercise.

        </div>

2.  Prepare the course for using Ansible.

    1.  Copy a skeleton directory structure for your Ansible files.

        ``` bash
        [user@host gl007]$ cp -r ~/rht-labs-core/docs/training/files/module_07/ansible .
        ```

    2.  Change into the `ansible/` directory.

        ``` bash
        [user@host gl007]$ cd ansible/
        ```

    3.  Create a directory for the exercise.

        ``` bash
        [user@host ansible]$ mkdir useRoles
        ```

3.  Use the `ansible-galaxy` command to create a new role named
    `gl007_motd`.

    1.  Create the role in the `ansible/roles/` directory.

        ``` bash
        [user@host ansible]$ ansible-galaxy role init --offline gl007_motd --init-path roles/
        - Role gl007_motd was created successfully
        ```

    2.  Display the directory structure of the new role.

        ``` bash
        [user@host ansible]$ tree roles/gl007_motd/
        roles/gl007_motd/
        ├── defaults
        │   └── main.yml
        ├── files
        ├── handlers
        │   └── main.yml
        ├── meta
        │   └── main.yml
        ├── README.md
        ├── tasks
        │   └── main.yml
        ├── templates
        ├── tests
        │   ├── inventory
        │   └── test.yml
        └── vars
            └── main.yml

        8 directories, 8 files
        ```

    3.  For this exercise, you do not need the `files`, `handlers`, and
        `vars` directories. Delete the directories.

        ``` bash
        [user@host ansible]$ rm -rf roles/gl007_motd/{files,handlers,vars}
        ```

4.  Customize the `gl007_motd` role.

    1.  Add variables in the `roles/gl007_motd/defaults/main.yml` file
        so that the file has the following content.

        ``` yaml
        ---
        # defaults file for gl007_motd
        filename: test
        mode: add
        exercise_title: ""
        message: This is a test message.
        ```

    2.  Create the message of the day template file at
        `roles/gl007_motd/templates/motd.j2`.

        ``` yaml
        {{ exercise_title }}
        {{ message }}
        ```

    3.  Add two tasks to the `roles/gl007_motd/tasks/main.yml` file so
        that the file has the following content.

        ``` yaml
        ---
        # tasks file for gl007_motd
        - name: Create custom MOTD file
          template:
            src: motd.j2
            dest: /etc/motd.d/{{ filename }}
          when: mode | lower == "add"

        - name: Remove custom MOTD file
          file:
            path: /etc/motd.d/{{ filename }}
            state: absent
          when: mode | lower == "remove"
        ```

    4.  The `meta/main.yml` file for your role contains information
        mostly applicable to Ansible Galaxy. Although we will not
        publish our roles to Ansible Galaxy, the `min_ansible_version`
        and `dependencies` variables help ensure that your role can be
        used successfully in different classroom environments. For this
        training module, customize the `roles/gl007_motd/meta/main.yml`
        file to specify your name and a brief description.

        ``` yaml
        galaxy_info:
          author: your name
          description: Creates or removes a custom MOTD file in /etc/motd.d/.
          company: Red Hat

        ...output omitted...
        ```

    5.  It can be easy to ignore the importance of the `README.md` file
        for your role. Customizing this file can help you identify ways
        that you can improve your role. For example, if a variable is
        required, does the role provide a default value in either
        `defaults/main.yml` or `vars/main.yml`? If a variable can only
        have specific values, does your role check for those values and
        provide an appropriate error message if the variable does not
        have the correct value?

        The `Example Playbook` section provides an example of how other
        developers can use your role as part of their guided exercise.

        For this training module, copy the
        `~/rht-labs-core/docs/training/files/module_07/README.md` file
        to the `roles/gl007_motd/README.md` file.

        ``` bash
        [user@host ansible]$ cp ~/rht-labs-core/docs/training/files/module_07/README.md roles/gl007_motd/README.md
        ```

    6.  Customize the `useRoles/use-test-role.yml` playbook with the
        following changes. Add a name to the playbook. Remove the
        `remote_user` line. Enable privilege escalation. Pass variable
        values to the role for the `exercise_title`, `message`, and
        `filename` variables.

        ``` yaml
        ---
        - name: Create custom MOTD file
          hosts: localhost
          become: True
          roles:
            - role: gl007_motd
              filename: use-roles
              exercise_title: "Developing Exercises Using Ansible Playbooks and Roles"
              message: "Custom MOTD message."
        ```

        <div class="important">

        There are several ways to pass variable values to roles. This
        example overrides variables by passing variable values to the
        role from the playbook. As long as the `filename` variable is
        not overridden from the command line or in the python script,
        the file that is created with `mode=add` will be deleted with
        `mode=remove`.

        </div>

5.  Configure the local environment for testing, and then test the
    `gl007_motd` role.

    1.  Although the lab grading framework automatically detects
        directories where roles can be installed, those directories are
        not checked for local testing. Run the
        `~/rht-labs-core/rolespath.py` python script, and use the script
        output to set the `DEFAULT_ROLES_PATH` environment variable.

        ``` bash
        [user@host ansible]$ source ~/.venv/labs/bin/activate
        (labs) [user@host ansible]$ DEFAULT_ROLES_PATH=$(python ~/rht-labs-core/rolespath.py)
        ```

        <div class="important">

        Whether or not role paths should be automatically detected or
        explicitly specified in a file such as
        `ansible/roles/requirements.yml` is still undecided. For this
        training module, using the `rolespath.py` python script is
        sufficient.

        If you have difficulty executing the `rolespath.py` script, or
        if the following `ansible-playbook` command complains about not
        finding the `gl007_motd` role, then temporarily add the
        `roles_path = ./roles` line to the `[defaults]` section of the
        `ansible/ansible.cfg` file.

        </div>

    2.  Run the `use-test-role.yml` playbook from the main `ansible/`
        directory.

        ``` bash
        (labs) [user@host ansible]$ ansible-playbook useRoles/use-test-role.yml

        PLAY [Create custom MOTD file] ********************************

        TASK [gl007_motd : Create custom MOTD file] *******************
        changed: [localhost]

        TASK [gl007_motd : Remove custom MOTD file] *******************
        skipping: [localhost]

        PLAY RECAP ****************************************************
        localhost                  : ok=1    changed=1    unreachable=0
        failed=0    skipped=1    rescued=0    ignored=0
        ```

    3.  Display the content of the `/etc/motd.d/use-roles` file. Notice
        that the template replaced both the `exercise_title` and
        `message` variables with the values passed to the role.

        ``` bash
        (labs) [user@host ansible]$ cat /etc/motd.d/use-roles
        Developing Exercises Using Ansible Playbooks and Roles
        Custom MOTD message.
        ```

    4.  Delete the file created previously by running the
        `use-test-role.yml` playbook with the `-e mode=remove` option.

        ``` bash
        (labs) [user@host ansible]$ ansible-playbook useRoles/use-test-role.yml -e mode=remove

        PLAY [Create custom MOTD file] ********************************

        TASK [gl007_motd : Create custom MOTD file] *******************
        skipping: [localhost]

        TASK [gl007_motd : Remove custom MOTD file] *******************
        changed: [localhost]

        PLAY RECAP ****************************************************
        localhost                  : ok=1    changed=1    unreachable=0
        failed=0    skipped=1    rescued=0    ignored=0
        ```

6.  Improve the `gl007_motd` role by ensuring that the `mode` variable
    is set to one of the expected values.

    1.  Verify that the two existing tasks are ignored if the
        `mode=create` variable is used.

        ``` bash
        (labs) [user@host ansible]$ ansible-playbook useRoles/use-test-role.yml -e mode=create

        PLAY [Create custom MOTD file] ********************************

        TASK [gl007_motd : Create custom MOTD file] *******************
        skipping: [localhost]

        TASK [gl007_motd : Remove custom MOTD file] *******************
        skipping: [localhost]

        PLAY RECAP ****************************************************
        localhost                  : ok=0    changed=0    unreachable=0
        failed=0    skipped=2    rescued=0    ignored=0
        ```

        <div class="important">

        Because the playbook did not fail, a developer running the
        playbook this way might be misled into believing that the
        playbook succeeded. It did not.

        </div>

    2.  Add a task to the `roles/gl007_motd/tasks/main.yml` file that
        generates a failure if the `mode` variable does not have value
        of either `add` or `remove`.

        ``` yaml
        ---
        # tasks file for gl007_motd
        - name: Fail if mode variable is not "add" or "remove"
          fail:
            msg: The "mode" variable must have a value of either "add" or "remove".
          when: mode | lower != "add" and mode | lower != "remove"

        - name: Create custom MOTD file
          template:
            src: motd.j2
            dest: /etc/motd.d/{{ filename }}
          when: mode | lower == "add"

        - name: Remove custom MOTD file
          file:
            path: /etc/motd.d/{{ filename }}
            state: absent
          when: mode | lower == "remove"
        ```

    3.  Verify that the playbook fails when the `mode=create` variable
        is used.

        ``` bash
        (labs) [user@host ansible]$ ansible-playbook useRoles/use-test-role.yml -e mode=create

        PLAY [Create custom MOTD file] ********************************************

        TASK [gl007_motd : Fail if mode variable is not "add" or "remove"]
        fatal: [localhost]: FAILED! => {"changed": false, "msg": "The \"mode\"
        variable must have a value of either \"add\" or \"remove\"."}

        PLAY RECAP ****************************************************************
        localhost                  : ok=0    changed=0    unreachable=0    failed=1
        skipped=0    rescued=0    ignored=0
        ```

7.  Customize the `use-roles.py` python script to run your playbooks for
    the start function.

    1.  Change to the `~/rht-labs-gl007/src/gl007/` directory.

        ``` bash
        (labs) [user@host ansible]$ cd ~/rht-labs-gl007/src/gl007/
        ```

    2.  Edit the `use-roles.py` script, and make the following changes.
        Update information under the CHANGELOG to match the following.

        ``` python
        ...output omitted...
        """Grading module for GL007:
        Guided Exercise: Developing Exercises Using Ansible Playbooks and Roles.
        This module provides functions for: start|finish
        """
        ...output omitted...
        ```

    3.  Modify the three lines starting with `_playbook_`. Change the
        `_playbook_start` and `_playbook_finish` lines to reference the
        `use-test-role.yml` playbook. Comment out the `_playbook_grade`
        line. The three lines must match the following.

        ``` python
        ...output omitted...
        _playbook_start = "ansible/useRoles/use-test-role.yml"
        #_playbook_grade = "ansible/examplePlaybook/playbookGrade.yml"
        _playbook_finish = "ansible/useRoles/use-test-role.yml"
        ...output omitted...
        ```

    4.  Change the `ExamplePlaybook` class so that it matches the
        following.

        ``` python
        ...output omitted...
        class UseRoles(Default):
            """Activity class."""
            __LAB__ = 'use-roles'

            def start(self):
                """Prepare the system for starting the lab."""
                items = [
                    {
                        "label": "Checking lab systems",
                        "task": labtools.check_host_reachable,
                        "hosts": _targets,
                        "fatal": True
                    },
                    {
                        "label": "Customizing the Message of the Day",
                        "task": self.run_playbook,
                        "playbook": _playbook_start,
                    },
                ]
                userinterface.Console(items).run_items()

            def finish(self):
                """Perform post-lab cleanup."""
                items = [
                    {
                        "label": "Checking lab systems",
                        "task": labtools.check_host_reachable,
                        "hosts": _targets,
                        "fatal": True
                    },
                    {
                        "label": "Removing custom Message of the Day file",
                        "task": self.run_playbook,
                        "playbook": _playbook_finish,
                        "vars": {"mode": "remove"}
                    },
                ]
                userinterface.Console(items).run_items(action="Finishing")
        ```

        <div class="note">

        Although this example only runs one playbook for the start
        function and one playbook for the finish function, you might
        want to use multiple playbooks in order to provide students with
        more feedback on the actions the script is performing.

        Additionally, you might run blocks of python code in between
        your playbooks.

        </div>

8.  Verify that the `start` function of the `use-roles` exercise works
    as expected.

    1.  Run the `start` function for the `use-roles` exercise.

        ``` bash
        (labs) [user@host gl007]$ lab start use-roles

        Starting lab.

         · Checking lab systems ................................. SUCCESS
         · Customizing the Message of the Day ................... SUCCESS
        ```

    2.  Verify that the `/etc/motd.d/use-roles` file displays the
        correct content based on the variables passed to the role.

        ``` bash
        (labs) [user@host gl007]$ cat /etc/motd.d/use-roles
        Developing Exercises Using Ansible Playbooks and Roles
        Custom MOTD message.
        ```

9.  Verify that the `finish` function of the `use-roles` exercise works
    as expected.

    1.  Run the `finish` function for the `use-roles` exercise.

        ``` bash
        (labs) [user@host gl007]$ lab finish use-roles

        Finishing lab.

         · Checking lab systems ................................. SUCCESS
         · Removing custom Message of the Day file .............. SUCCESS
        ```

    2.  Verify that the `/etc/motd.d/use-roles` file no longer exists.

        ``` bash
        (labs) [user@host gl007]$ cat /etc/motd.d/use-roles
        cat: /etc/motd.d/use-roles: No such file or directory
        ```

This concludes this guided exercise.

# Using AutoPlay with Ansible Playbooks

Use the AutoPlay feature of the lab grading framework to minimize the
amount of python scripting needed to create an exercise.

Although AutoPlay minimizes the amount on python scripting, AutoPlay is
not appropriate for many exercises. Ask yourself the following questions
to help you decide if using AutoPlay is the right choice for your
exercise.

- Does the exercise need to use a hybrid of python code and Ansible
  playbooks?

  - **Yes**: Do not use AutoPlay

  - **No**: AutoPlay might be appropriate

- Can Ansible playbooks perform all of the start, grade, and finish
  tasks required for the exercise?

  - **Yes**: AutoPlay might be appropriate

  - **No**: Do not use AutoPlay

- Do you need the flexibility to display custom messages for your
  playbook?

  - **Yes**: Do not use AutoPlay

  - **No**: AutoPlay might be appropriate

- Are the tasks to start, grade, or finish complex enough that students
  would benefit from seeing multiple messages?

  - **Yes**: Do not use AutoPlay

  - **No**: AutoPlay might be appropriate

# Developing Exercises using AutoPlay

In this exercise, you will create files and directories in order to use
AutoPlay to run the start function of an exercise.

This exercise assumes that you completed the first two training modules.
You created a virtual environment in the
`01_DevelopmentEnvironment.adoc` training module. You created the
**GL007** course in the `02_DevelopmentLocalSourceCode.adoc` training
module.

1.  To use AutoPlay, you must create a python script that imports the
    `AutoPlay` class and defines a new class for your exercise. Change
    into the sample `gl007` directory.

    ``` bash
    (labs) [user@host ~]$ cd ~/rht-labs-gl007/src/gl007/
    ```

    Copy the `exampleAutoPlay.py` script from the **GL006** course to a
    new file named `use-autoplay.py`.

    ``` bash
    (labs) [user@host gl007]$ cp ~/rht-labs-core/packages-gl006/src/gl006/exampleAutoPlay.py use-autoplay.py
    ```

2.  Modify the new file, and change the name of the `ExampleAutoPlay`
    class to match the name of your python file. Class names use
    `CapWords` capitalization.

    ``` bash
    (labs) [user@host gl007]$ vim use-autoplay.py
    ```

    Change `ExampleAutoPlay` to `UseAutoPlay`, and change
    `example-autoplay` to `use-autoplay`.

    ``` python
    ...output omitted...
    from labs.grading import AutoPlay


    class UseAutoPlay(AutoPlay):
        __LAB__ = 'use-autoplay'
    ```

3.  Within the `ansible` directory, create a new directory for your
    exercise. The name of the directory must match the name of the
    associated python script without the `.py` suffix.

    ``` bash
    (labs) [user@host gl007]$ cd ~/rht-labs-gl007/src/gl007/ansible
    (labs) [user@host ansible]$ mkdir use-autoplay
    ```

4.  Change into the `use-autoplay` directory, and create `start.yml` to
    define the playbook used to start your exercise.

    1.  Change into the
        `~/rht-labs-gl007/src/gl007/ansible/use-autoplay/` directory.

        ``` bash
        (labs) [user@host ansible]$ cd use-autoplay/
        ```

    2.  Create a simple `start.yml` playbook with the following content.

        ``` yaml
        ---
        - name: Start tasks for the use-autoplay exercise
          hosts: localhost
          become: False
          gather_facts: False

          tasks:
            - name: Sample start task
              copy:
                content: "Sample start task.\n"
                dest: /tmp/use-autoplay.txt
        ```

        <div class="note">

        Although not performed in this exercise, you would also create
        `finish.yml` to define the playbook used to finish your
        exercise. If your exercise requires grading, then create the
        `grade.yml` playbook.

        </div>

5.  Run the start function for the `use-autoplay` exercise.

    ``` bash
    (labs) [user@host use-autoplay]$ lab start use-autoplay

    Starting lab.

     · Running Start Playbook ............................... SUCCESS
    ```

    <div class="note">

    When using AutoPlay, you do not have the ability to specify the
    display value for the task being run. The `AutoPlay` class uses the
    labels, `Running Start Playbook`, `Running Grade Playbook`, and
    `Running Finish Playbook`.

    </div>

6.  Verify that the `/tmp/use-autoplay.txt` file contains the specified
    content.

    ``` bash
    (labs) [user@host use-autoplay]$ cat /tmp/use-autoplay.txt
    Sample start task.
    ```

7.  Verify that the `use-autoplay` exercise does not provide finish
    functionality. If you want the exercise to provide finish
    functionality, then you must create the `finish.yml` playbook.

    ``` bash
    (labs) [user@host use-autoplay]$ lab finish use-autoplay
    The finish command is not supported for this lab.
    ```

This concludes this guided exercise.

## Next Steps

The next training module will help you to create tests for your Python
functions


