#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#

"""Lab grading script function library."""

import os
import shutil
import socket
import subprocess
import logging
import pkg_resources

from labs.laberrors import LabError
from labs import labconfig

SKU = labconfig.get_course_sku().upper()


def host_reachable(hosts_to_check, port="22"):
    """Test SSH connection with the given host.

    :param hosts_to_check: List of host to check (hostnames or IP addresses)
    :type hosts_to_check: list

    :returns: The list of unreachable hosts or an empty list if all the hosts
              are up.
    """
    unreachable_hosts = []
    for host in hosts_to_check:
        try:
            socket.setdefaulttimeout(10)
            s = socket.create_connection((host, port))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception:
            unreachable_hosts.append((host, port))

    return unreachable_hosts


def check_host_reachable(item):
    """Test SSH connection with the given host.

    This function is a wrapper around :py:func:`host_reachable` and is intended
    to be used by the lab modules through the
    :py:func:`common.labtools.run_items` function.

    :para item:
    :type item: dict

    :returns: 0 when all the given hosts are reachable or 1 when at least one
              host failed.
    """
    if "hosts" not in item:
        item["failed"] = False
        return 0
    failed_hosts = host_reachable(item["hosts"])
    if not failed_hosts:
        item["failed"] = False
        return 0
    item["failed"] = True
    item["msgs"] =\
        [{"text": f"{host} cannot be reached over port {port}"}
            for host, port in failed_hosts]
    return 1


# TODO: Are we going to scp/sftp/rsync files/dirs to other hosts?

def get_sku_path(path=""):
    """
    Get a path relative to ${HOME}/SKU
    """
    return os.path.join(os.path.expanduser("~"), SKU, path)


def mkdir(path):
    """
    Create directory
    """
    ret_val = {}
    if os.path.exists(path) and os.path.isdir(path):
        ret_val["failed"] = False
    else:
        try:
            os.makedirs(path)
            ret_val["failed"] = False
        except (OSError, PermissionError, FileExistsError) as e:
            ret_val["failed"] = True
            ret_val["msgs"] = [
                {"text": "Could not create directory: {}".format(path)}
            ]
            ret_val["exception"] = {
                "name": e.__class__.__name__,
                "message": str(e),
            }
    return ret_val


def rmdir(path, recursive=False):
    """
    Delete directory
    """
    ret_val = {}
    # Check if path begins with "/" and treat as absolute
    if not path.startswith("/"):
        path = get_sku_path(path)
    if os.path.exists(path):
        try:
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            ret_val["failed"] = False
        except Exception as e:
            ret_val["failed"] = True
            ret_val["msgs"] = [
                {"text": "Could not delete directory: {}".format(path)}
            ]
            ret_val["exception"] = {
                "name": e.__class__.__name__,
                "message": str(e),
            }
    else:
        ret_val["failed"] = False
    return ret_val


def touch(path, content):
    """
    Create file with a given content
    """
    ret_val = {}
    try:
        with open(path, 'w') as file:
            file.write(content)
        ret_val["failed"] = False
    except Exception as e:
        ret_val["failed"] = True
        ret_val["msgs"] = [
            {"text": "Could not write file: {}".format(path)}
        ]
        ret_val["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }
    return ret_val


# TODO: implement recursive dir copy
def cp(source, destination):
    """
    Copy file
    """
    ret_val = {}
    destination = get_sku_path(destination)
    try:
        shutil.copy(source, destination)
        ret_val["failed"] = False
    except Exception as e:
        ret_val["failed"] = True
        ret_val["msgs"] = [
            {"text": "Could not copy file to: {}".format(destination)}
        ]
        ret_val["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }
    return ret_val


def mv(source, destination):
    """
    Move file
    """
    ret_val = {}
    try:
        shutil.move(source, destination, copy_function=shutil.copy)
        ret_val["failed"] = False
    except Exception as e:
        ret_val["failed"] = True
        ret_val["msgs"] = [
            {"text": "Could not move file to: {}".format(destination)}
        ]
        ret_val["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }
    return ret_val


def rm(path):
    """
    Delete file(s)
    """
    ret_val = {}
    if isinstance(path, list):
        for item in path:
            return rm(item)
    else:  # isinstance(path, str):
        try:
            os.remove(path)
            ret_val["failed"] = False
        except Exception as e:
            ret_val["failed"] = True
            ret_val["msgs"] = [
                {"text": "Could not delete file: {}".format(path)}
            ]
            ret_val["exception"] = {
                "name": e.__class__.__name__,
                "message": str(e),
            }
    return ret_val


def grep(path, content):
    """
    Look for a string in a file
    """
    ret_val = {}
    try:
        with open(path, "r") as file:
            for line in file:
                if content in line:
                    ret_val["failed"] = False
        if ret_val.get("failed", None) is not False:
            raise LabError
    except Exception as e:
        ret_val["failed"] = True
        ret_val["msgs"] = [
            {
                "text": "File does not contain string: {}".format(path)
            }
        ]
        ret_val["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }

    return ret_val


def ping(host, af="IPv4", timeout=2):
    """
    ICMP ping a host via IPv4 or IPv6
    """
    ret_val = {}
    if af == "IPv4":
        ping_command = "ping"
    else:  # af == "IPv6"
        ping_command = "ping6"
    try:
        subprocess.run(
            [ping_command, "-c", "1", host],
            timeout=timeout,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        ret_val["failed"] = False
    except Exception as e:
        ret_val["failed"] = True
        ret_val["msgs"] = [{"text": "Could not ping host: {}".format(host)}]
        ret_val["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }

    return ret_val


def delete_workdir(item):
    """
    Remove ~/SKU/{labs,solutions}/lab_name directories
    """
    try:
        for dir in ["labs", "solutions"]:
            lab_dir = os.path.join(
                os.path.expanduser("~"), SKU, dir, item["lab_name"]
            )
            logging.info("Delete directory: {}".format(lab_dir))
            if not rmdir(lab_dir, recursive=True):
                item["failed"] = True
                item["msgs"] = [{"text": "Directory could not be removed"}]
                return

    except Exception as e:
        item["msgs"] = [
            {"text": "Could not delete materials directories: %s" % e}
        ]
        item["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }
        item["failed"] = True


def copy_lab_files(item):
    """
    Copy files into ~/SKU/labs/exercise and ~/SKU/solutions/exercise
    """
    lab_full_name = "{}.{}".format(SKU.lower(), item['lab_name'])
    try:
        for lab_dir in ["labs", "solutions"]:
            src = os.path.join("materials", lab_dir,
                               item['lab_name'])
            src = pkg_resources.resource_filename(lab_full_name, src)
            student_path = os.path.join(get_sku_path(), lab_dir,
                                        item['lab_name'])

            copy_or_replace_dir(src, student_path)
    except Exception as e:
        item["msgs"] = [{"text": "Could not copy files: %s" % e}]
        item["exception"] = {
            "name": e.__class__.__name__,
            "message": str(e),
        }
        item["failed"] = True


def copy_or_replace_dir(source: str, destination: str, no_source_error=False):
    """
    Copy a directory from the "source" path to "destination" path
    If the destination exists, replace the directory.

    If "no_source_error" is True, raise an exception
    if the source does is not a directory
    """
    if os.path.isdir(source):
        if os.path.isdir(destination):
            shutil.rmtree(destination)
        shutil.copytree(src=source, dst=destination)

    elif no_source_error:
        raise OSError(f"{source} is not a directory or does not exist")
