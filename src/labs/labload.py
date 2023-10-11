# Lab Dynamic Loading
#
# Jim Rigsbee <jrigsbee@redhat.com>
# (C)opyright 2021 : Red Hat, Inc. - see LICENSE
#
import logging
import traceback
import os
import pathlib
import pkgutil
import inspect
import importlib

import requests

from labs.grading import Default
from labs.laberrors import LabError
from labs.lablog import lablog_init
from labs import labconfig


def loadcache():
    course = labconfig.get_course_sku()
    cache = {}
    try:
        module = importlib.import_module(course)
        modules = [name for _, name, _
                   in pkgutil.iter_modules([os.path.dirname(module.__file__)])]
        if len(modules) == 0:
            return cache
        for m in modules:
            s = importlib.import_module(course + '.' + m)
            c = [obj for _, obj in inspect.getmembers(s, inspect.isclass)]
            for x in c:
                if x.__name__ != 'Default' and x.__name__ != 'AutoPlay'\
                   and Default in inspect.getmro(x):
                    script = x.__name__
                    if "__LAB__" in x.__dict__.keys():
                        script = x.__LAB__
                    entry = {
                        "class": x.__name__,
                        "module": m
                    }
                    cache[script] = entry
    except ModuleNotFoundError:
        if 'm' in locals():
            print("Could not find module %s for course %s"
                  % (m, course))
        else:
            print("Could not find modules for course %s" % course)

        logging.critical(traceback.format_exc())
        return {}
    return cache


def get_all_lab_scripts(ctx, args, incomplete):
    return sorted(get_classes(ctx, args, incomplete) + get_bash_scripts())


def get_classes(ctx, args, incomplete):
    cache = loadcache()
    classes = [script
               for script in cache.keys()
               if not incomplete or incomplete in script]
    return classes


def get_bash_scripts():
    # This emulates /usr/share/bash-completion/completions/lab.
    #
    # First, we check if that path is present. The lab completion existence is
    # used as a test that traditional lab scripts are installed in the
    # environment.
    #
    # If it's not there, then we say that there are no traditional lab scripts
    # installed, and exit, so the rest of this function does not execute. Thus,
    # we don't perform any additional checking, and we assume that the lab
    # environment is properly setup.
    if not pathlib.Path("/usr/share/bash-completion/completions/lab").exists():
        return []

    with open("/etc/rht") as rht_file:
        rht_lines = rht_file.readlines()

    def _get_var(name):
        # get the last line that starts with name, return what's left of the =
        return [line.strip().split("=", 2)[1]
                for line in rht_lines
                if line.startswith(name)][-1]

    rht_course = _get_var("RHT_COURSE")
    rht_vmtree = _get_var("RHT_VMTREE")

    # rht_vmtree is "ocp4.6/x86_64" (with quotes), we want ocp4.6
    version = rht_vmtree[1:-1].split("/")[0]

    grading_scripts_url = (
        "http://content.example.com/courses/"
        f"{rht_course}/{version}" +
        "/grading-scripts/"
    )

    html_listing = requests.get(grading_scripts_url).text
    html_lines = html_listing.split("\n")
    file_lines = [line for line in html_lines if '[TXT]' in line]
    file_texts = [line.split('"')[7] for line in file_lines]
    return [file_text[4:]
            for file_text in file_texts
            if file_text.startswith("lab-")]


def is_course_installed(sku):
    try:
        importlib.import_module(sku.lower())
        return True
    except ModuleNotFoundError:
        return False


def import_grading_library(config, name):
    """
    Imports the grading library. Takes a single parameter
    :param name:
    :return:
    """
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
