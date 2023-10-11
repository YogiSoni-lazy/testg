#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#

"""Run Ansible Playbooks."""

import os
import tempfile
import ansible_runner
import importlib
import logging
import pkg_resources

from labs import labconfig


class Runner:
    """Run Ansible Playbooks.

    :param playbook_path: Full path to the Ansible Playbook to run.
    :type playbook_path: str
    """

    def __init__(self, playbook_path):
        """Initialize the object."""
        self.playbook_path = playbook_path
        self.playbook_file = os.path.basename(playbook_path)
        self.playbook_dir = os.path.dirname(playbook_path)
        self.playbook_dir_name = os.path.basename(self.playbook_dir)
        self.playbook_dir_file = os.path.join(self.playbook_dir_name,
                                              self.playbook_file)
        self.parent_rel_dir = os.path.join(self.playbook_dir, os.pardir)
        self.playbook_parent_dir = os.path.abspath(self.parent_rel_dir)

    def run(self, vars={}, inventory=None):
        """Run the Ansible Playbook.

        :param vars: A dictionary of variables to use during playbook
                     execution.
        :type vars: dict, optional

        :param inventory: An inventory location (file or directory) to use, if
                          the default inventory should not be used.
        :type inventory: str, optional

        :raises OSError: Cannot change directory to the playbook directory or
                         missing playbook.

        :returns: If some task fails, the list of error messages. Otherwise,
                  when the playbook completes successfully, an empty list.
        """
        kwargs = {}
        if inventory:
            kwargs['inventory'] = inventory

        if not os.path.isfile(self.playbook_path):
            raise FileNotFoundError(2, "No such file or directory",
                                    self.playbook_path)

        save_cwd = os.getcwd()
        os.chdir(self.playbook_parent_dir)

        roles_path = self.discover_roles_path()
        ret_messages = []
        with tempfile.TemporaryDirectory() as tmp_dir:
            r = ansible_runner.run(
                project_dir=self.playbook_parent_dir,
                playbook=self.playbook_dir_file,
                private_data_dir=tmp_dir,
                settings={"suppress_ansible_output": True},
                extravars=vars,
                roles_path=roles_path,
                **kwargs,
            )
            if r.rc != 0:
                for event in r.events:
                    if event["event"] == "runner_on_failed":
                        host = event["event_data"]["host"]
                        task = event["event_data"]["task"]
                        msg = event["event_data"]["res"]["msg"]
                        ret_messages.append(f"{host}: {task}: {msg}")
                        # TODO: Complete output of the ansible run.
                        # That file should probably be copied in the log
                        # file or directory.
                        os.path.join(
                            tmp_dir, "artifacts",
                            event["runner_ident"], "stdout"
                        )
                    if "stdout" in event:
                        logging.error(event["stdout"])
                if not ret_messages:
                    ret_messages.append("Failed to run the playbook.")

        os.chdir(save_cwd)
        return ret_messages

    def discover_roles_path(self):
        roles_path = []
        sku = labconfig.get_course_sku()
        sku_role_path = self._locate_ansible_path(sku)
        if sku_role_path:
            roles_path.append(sku_role_path)

        _package = pkg_resources.working_set.by_key["rht-labs-" + sku.lower()]
        for dependency in _package.requires():
            if "rht-labs-" in dependency.name:
                logging.debug("Processing package %s to find Ansible roles"
                              % dependency.name)
                mod_path =\
                    self._locate_ansible_path(dependency.name.split('-')[-1])
                if mod_path:
                    roles_path.append(mod_path)

        logging.debug("Ansible roles path is %s" % roles_path)
        return roles_path

    def _locate_ansible_path(self, module_name):
        path = None
        try:
            module = importlib.import_module(module_name)
            if "__ANSIBLE_ROLES_PATH__" in module.__dict__:
                path = module.__dict__["__ANSIBLE_ROLES_PATH__"]
        except ModuleNotFoundError:
            pass
        return path
