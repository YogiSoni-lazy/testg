from labs.ui import GradingStep
from labs.ui.steps import ansible

from labs.activities import GuidedExercise


class ErrorMessages(GuidedExercise):
    __LAB__ = "error-messages"

    def grade(self):
        ansible.run_playbook_step(
            self,
            "test.yml",
            tags=["regular_error"],
            step_message="Display a regular playbook error message",
            grading=True,
        )

        ansible.run_playbook_step(
            self,
            "test.yml",
            tags=["new_error"],
            step_message="Display a new playbook error message",
            step_type=GradingStep,
        )

        ansible.run_playbook_step(
            self,
            "test.yml",
            tags=["regular_loop_errors"],
            step_message="Display regular playbook error messages for a loop",
            step_type=GradingStep,
            extra_vars={"required_packages": "{{ container_packages }}",
                        "some_var": "false"},
        )

        ansible.run_playbook_step(
            self,
            "test.yml",
            tags=["new_loop_errors"],
            step_message="Display new playbook error messages for a loop",
            step_type=GradingStep,
        )
