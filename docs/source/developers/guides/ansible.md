# Using Ansible

You can use the {py:func}`labs.ui.steps.ansible.run_playbook_step` function to invoke Ansible steps from any lab script.

For example, if you have a grading script in `classroom/grading/src/sku/exercise.py`, you can add calls to this function as follows:

```
from labs.ui.steps import ansible
from labs.activities import GuidedExercise

class ExampleLabScript(GuidedExercise):
    __LAB__ = "intro-prepare"

    def start(self):
        ansible.run_playbook_step(
            self,
            "common/manage-package.yml",
            step_message="Removing exercise software",
            extra_vars={
                "mode": "remove",
                "packages": "{{ intro_prepare_remove }}",
            },
        )
```

You must put your Ansible project in the `/classroom/grading/src/sku/ansible` path within your course repository.
This directory must contain an `ansible.cfg` file.
Paths to playbooks, such as `comon/manage-package.yml` are relative to this directory.

For further details, review the {py:func}`labs.ui.steps.ansible.run_playbook_step` documentation.
