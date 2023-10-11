import pkg_resources
import os
import logging
from labs.common import userinterface

# Not all systems support Ansible playbooks (e.g. Windows)
try:
    from labs.common import playbooks
except ModuleNotFoundError:
    logging.info("Ansible playbooks not supported in this system")


class Default:
    def __init__(self):
        pass

    def start(self):
        """lab start

        Override this method to define the start logic
        """
        print('The start command is not supported for this lab.')

    def finish(self):
        """lab finish

        Override this method to define the finish logic
        """
        print('The finish command is not supported for this lab.')

    def grade(self):
        """lab grade

        Override this method to define the grade logic
        """
        print('The grade command is not supported for this lab.')

    def fix(self):
        """lab fix

        Override this method to define the fix/solve logic
        """
        print('The fix command is not supported for this lab.')

    def run_playbook(self, item):
        """Execute the playbook.

        :param item: A dictionary that describes a lab grading script
                     step to run.  The dictionary must contain either
                     a "playbook" attribute, or a "playbookPath" attribute.

                     An optional "inventory" attribute can specify the location
                     of an inventory to use with the playbook.

                     An optional "vars" attribute can contain a dictionary of
                     key/values to use as variable input to the playbook.
        :type item: dict

        """
        if "playbookPath" in item:
            playbook_path = item["playbookPath"]
        else:
            playbook_path = self.find_playbook(item["playbook"])

        runner = playbooks.Runner(playbook_path)

        kwargs = {}
        if "vars" in item:
            kwargs['vars'] = item["vars"]
        if "inventory" in item:
            kwargs["inventory"] = item["inventory"]

        messages = runner.run(**kwargs)
        if messages:
            item["failed"] = True
            item["msgs"] = [{"text": "Playbook failed: "
                            + os.path.basename(playbook_path)}]
            for msg in messages:
                item["msgs"].append({"text": msg})
        else:
            item["failed"] = False

    def find_playbook(self, playbook, fixed=False):
        """
        Find the playbook in a standard location.
        """
        if fixed:
            class_module = self.__module__.split(".")[1]
            playbook = "ansible/" + class_module + "/" + playbook

        playbook_path =\
            pkg_resources.resource_filename(self.__module__,
                                            playbook)

        return playbook_path


class AutoPlay(Default):
    def __init__(self):
        pass

    def start(self):
        """
        Automatically locate the start playbook, if one exists,
        and run it.
        """
        playbook_path = self.find_playbook("start.yml", fixed=True)
        if not os.path.exists(playbook_path):
            super().start()
            return

        items = [
            {
                "label": "Running Start Playbook",
                "task": self.run_playbook,
                "playbookPath": playbook_path,
            },
        ]
        userinterface.Console(items).run_items()

    def grade(self):
        """
        Automatically locate the grade playbook, if one exists,
        and run it.
        """
        playbook_path = self.find_playbook("grade.yml", fixed=True)
        if not os.path.exists(playbook_path):
            super().grade()
            return

        items = [
            {
                "label": "Running Grade Playbook",
                "task": self.run_playbook,
                "playbookPath": playbook_path,
            },
        ]
        ui = userinterface.Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()

    def finish(self):
        """
        Automatically locate the finish playbook, if one exists,
        and run it.
        """
        playbook_path = self.find_playbook("finish.yml", fixed=True)
        if not os.path.exists(playbook_path):
            super().finish()
            return

        items = [
            {
                "label": "Running Finish Playbook",
                "task": self.run_playbook,
                "playbookPath": playbook_path,
            },
        ]
        userinterface.Console(items).run_items(action="Finishing")
