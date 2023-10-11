#!/usr/bin/env python

"""
CLI for Red Hat Training lab generator

Create a new lab package for a given course
"""

import os
import pwd
import click
import jinja2


from labs import version


@click.command()
@click.argument("sku", required=True)
@click.argument("root", required=True)  # path to the curse git repo
def create_package(sku, root):
    """
    Create a new lab package for a given course

    SKU is the course code, such as gl006

    ROOT is the path to the course git repository
    """
    print("Creating directory: %s" % root)

    print("Creating labs package for %s" % sku)
    lab_sku_dir = root + "/src/" + sku.lower()
    os.makedirs(lab_sku_dir)

    templater = Templater(sku)
    templater.generate("setup.cfg.j2", root + "/setup.cfg")
    templater.generate("setup.py.j2", root + "/setup.py")
    templater.generate("MANIFEST.in.j2", root + "/MANIFEST.in")
    templater.generate("README.md.j2", root + "/README.md")
    templater.generate("LICENSE", root + "/LICENSE")
    templater.generate("src/sku/version.py", lab_sku_dir + "/version.py")
    templater.generate("src/sku/__init__.py", lab_sku_dir + "/__init__.py")

    print("Lab package is located in the: " + root + " directory")


@click.command()
@click.argument("sku", required=True)
@click.argument("root", required=True)
@click.argument('name', required=True)
@click.option("--template", default='python',
              type=click.Choice(
                  ['openshift', 'playbook', 'autoplay',
                   'python']
              ),
              help="Template to generate the lab script."
              " Defaults to python.")
def add_script(name, sku, root, template):
    """
    Create a new lab package for a given course

    SKU is the course code, such as gl006

    ROOT is the path to the course git repository
    """

    templates = {
        "openshift":    "template-openshift",
        "playbook":     "template-playbook",
        "autoplay":     "template-autoplay",
        "python":       "template-python",

    }

    if template not in templates.keys():
        print("Template %s not found, aborting" % template)
        return

    lab_sku_dir = "%s/src/%s" % (root, sku.lower())

    (n1, n2) = name.split("-")
    class_name = ''.join([n1.capitalize(), n2.capitalize()])

    script_name = "%s/%s.py" % (lab_sku_dir, name)
    templater = Templater(sku)
    templater.generate("src/sku/" + templates[template] + ".py.j2",
                       script_name,
                       class_name=class_name,
                       name=name)

    print("The new lab script is located at %s" % script_name)


@click.group(name='lab-generator', invoke_without_command=False)
@click.pass_context
def main(ctx):
    """
    CLI for Red Hat Training lab generator
    """

    if ctx.invoked_subcommand is None:
        print("No command specified.")


main.add_command(create_package)
main.add_command(add_script)


class Templater:
    def __init__(self, sku):
        self.template_loader = jinja2.PackageLoader(
            package_name="lab_generator",
            package_path="templates",
        )
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.sku = sku
        username = os.getenv("USER")
        self.author = pwd.getpwnam(username).pw_gecos
        self.author_email = "%s@redhat.com" % pwd.getpwnam(username).pw_name

    def generate(self, template, path, **kwargs):
        template = self.template_env.get_template(template)
        template.stream(
            sku=self.sku,
            author=self.author,
            author_email=self.author_email,
            core_version=version.__version__,
            **kwargs,
        ).dump(path)


if __name__ == '__main__':
    main()
