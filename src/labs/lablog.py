# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.

"""
Initialize the logging framework.

This module configures the Python logging framework to log messages in a
log file. Additionally, it can capture the stdout and stderr streams and
duplicate them in the log file.

Once initialized, guided exercises and lab developers can simply use the
default Python framework within their code. For example::

    import logging
    logging.debug("Initiating API call")
    logging.info("Start grading")
    logging.warning("API is very slow to reply")
    logging.error("Student failed to complete the exercise")
    logging.critical("The lab script cannot be found")

DynoLabs developers can create a sub non-root logger if they want to.

The module provides two functions:

* :func:`lablog_init` which is used to initialize the framework. This function
  should be called once, at the beginning of the program.
* :func:`run_capture` which calls :func:`subprocess.run` but duplicates the
  stdout and stderr stream in the log file. Developers may use this function
  instead of :func:`subprocess.run` when they want that stream captured.

.. seealso:: `Logging HOWTO <https://docs.python.org/3/howto/logging.html>`_
"""

import os
import sys
import logging
import pathlib
import tempfile
import datetime
import subprocess
from typing import Dict, Optional

# File stream of the log file
_log_file = None
# Are stdout and stderr captured in the log file?
_log_capture = False
# Backup stdout and stderr
_save_stdout = sys.stdout
_save_stderr = sys.stderr


class _DupToLog:
    """
    Duplicate an output stream to a file.

    :param log_stream: :term:`File object <file object>` where the output must
                       be duplicated.
    :type log_stream: File object
    :param file_obj: Output file object to duplicate (``sys.stdout``
                     for example)
    :type file_obj: File object
    """

    def __init__(self, log_stream, file_obj):
        """
        Initialize the object.
        """
        self.log_stream = log_stream
        self.f = file_obj

    def write(self, data):
        """
        Write the given data to both the output stream and the file.

        :param data: Data to write.
        :type data: str
        :return: The number of characters written.
        :rtype: int
        """
        self.log_stream.write(data)
        self.log_stream.flush()
        return self.f.write(data)

    def __getattr__(self, name):
        """
        Call unknown methods from the file object (flush, close, ...).
        """
        return getattr(self.f, name)


def lablog_init(config, lab_name):
    """
    Initialize the Python logging framework.

    Uses the configuration parameters under the ``logging`` section of the
    configuration file to configure the Python logging framework.

    The following parameters from the ``logging`` section are used:

    * ``level`` indicates the log level. Messages with a lower level are not
      stored in the log file. The accepted values are: ``debug``, ``info``,
      ``warning``, ``error``, or ``critical`` (case insensitive).
      When ``level`` is ``debug``, the stdout and stderr streams are also
      captured in the log file.
    * ``path`` provides the log file path and name. All the intermediate
      directories are created if needed. If the parameter ends with a ``/``
      character, then the log file name is built from that path with the lab
      name appended. The given path can include some special patterns that are
      substituted:

      * ``{lab_name}`` is replaced by the lab name. For example, if the path is
        ``/var/tmp/{lab_name}.out``, and the lab name is ``lab_01_1``, then the
        log file is :file:`/var/tmp/lab_01_1.out`.
      * A time and date with the same format as the
        :func:`datetime.date.strftime` method.
        See `strftime() and strptime() Behavior
        <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`_.
        For example, if the path is ``/var/tmp/{lab_name}.%Y%m%d-%H%M``, then
        the log file is :file:`/var/tmp/lab_01_1.20201201-2046` (when the lab
        name is ``lab_01_1`` and the current date and time are 1 december
        2020 20h46)

      If the log file already exists, then its is opened in append mode,
      otherwise it is created.
    * ``capture_output`` specifies whether stdout and stderr should be
      captured in the log file. If not set, the parameter defaults to ``False``
      unless ``level`` is ``debug``.

    If the configuration file has no ``logging`` section, then logging is
    completely disabled (no messages are logged).

    :param config: The configuration object (see :mod:`labs.labconfig`)
    :type config: dict
    :param lab_name: Name of the lab as provided by the student
                     with the :command:`lab` command.
    :type lab_name: str

    :raises OSError: When the log file or its parent directory
                     cannot be accessed or created.
    """
    global _log_file, _log_capture
    _config = config['rhtlab']
    if "logging" not in _config:
        logging.disable()
        return

    # If the lablog_init function has already been called, then close the
    # log file.
    if _log_file is not None:
        _log_file.close()
        # The 'force' parameter of logging.basicConfig() removes the handlers.
        # However, that option is only available since Python 3.8. Therefore,
        # the following code removes the handlers.
        root = logging.getLogger("")
        for h in root.handlers[:]:
            root.removeHandler(h)
            h.close()

    if _log_capture:
        _log_capture = False
        sys.stdout = _save_stdout
        sys.stderr = _save_stderr

    log_level = logging.INFO
    log_path = None

    # Retrieve parameters from the configuration object
    if isinstance(_config["logging"], dict):
        if "level" in _config["logging"]:
            log_level = configure_log_level(
                _config["logging"],
                log_level
            )
        if "path" in _config["logging"]:
            log_path = configure_logging_path(_config["logging"], lab_name)
        configure_logging_output(_config["logging"], log_level)

    # Open the log file in append mode. If the "path" parameter is not given
    # in the configuration, then, as a fallback, create a temporary file for
    # logging.
    if log_path:
        _log_file = open(log_path, "a")
    else:
        _log_file = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", prefix=lab_name, delete=False
        )

    if _log_capture:
        sys.stdout = sys.stderr = _DupToLog(_log_file, _save_stdout)

    logging.basicConfig(
        stream=_log_file,
        # encoding="utf-8", # Not before 3.9
        # force=True,       # Not before 3.8
        level=log_level,
        format=f"%(asctime)s:{lab_name}:%(levelname)s:%(filename)s(%(lineno)d)\
                %(message)s"
    )
    logging.info("#" * 20 + f" {lab_name} " + "#" * 20)


def configure_log_level(config_logging, log_level):
    """
    Retrieve  the log level from the configuration object
    """
    configured_log_level = config_logging["level"].upper()

    if configured_log_level.startswith("DEB"):
        log_level = logging.DEBUG
    elif configured_log_level.startswith("INFO"):
        log_level = logging.INFO
    elif configured_log_level.startswith("WARN"):
        log_level = logging.WARNING
    elif configured_log_level.startswith("ERR"):
        log_level = logging.ERROR
    elif configured_log_level.startswith("CRI"):
        log_level = logging.CRITICAL

    return log_level


def configure_logging_path(config_logging: Dict, lab_name: str):
    """
    Retrieve the path to the log file from the configuration object
    and ensure the directory exists
    """
    log_path = get_logging_path(config_logging, lab_name)

    pathlib.Path.mkdir(log_path.parent, parents=True, exist_ok=True)

    return log_path


def get_logging_path(config_logging: Dict, lab_name: Optional[str]):
    """
    Retrieve the path to the log file from the configuration object
    """
    logging_path = (
        datetime.datetime.now()
        .strftime(config_logging["path"])
        .format(lab_name=lab_name)
    )

    path_ends_with_separator = logging_path.rstrip()[-1] == os.sep

    if path_ends_with_separator and lab_name:
        log_path = pathlib.Path(logging_path) / lab_name
    else:
        log_path = pathlib.Path(logging_path)

    return log_path


def read_log_lines(logging_config: Dict, lab_name: Optional[str]):
    """
    Read a log file line by line.
    If lab_name is passed,
    then the function reads the logs of a specific lab
    """
    log_file_path = get_logging_path(logging_config, lab_name)

    with open(log_file_path) as f:
        return f.readlines()


def configure_logging_output(config_logging, log_level):
    """
    Retrieve from the configuration object whether stdout/stderr
    must be captured in the log file (capture_output)
    """
    global _log_capture

    if "capture_output" in config_logging:
        _log_capture = config_logging["capture_output"]
    elif log_level == logging.DEBUG:
        _log_capture = True

    return _log_capture


def run_capture(*args, **kwargs):
    """
    Execute :func:`subprocess.run` and capture the output in the log file.

    Developers should call this function instead of :func:`subprocess.run` when
    running an external command. This way, the external command outputs are
    saved in the log file (if the ``capture_output`` configuration file
    parameter is ``True`` or the ``level`` is ``debug``)

    The function signature is the same as the :func:`subprocess.run` function.
    It accepts the same parameters, returns the same values, and raises the
    same exceptions.

    .. seealso: `Subprocess management
    <https://docs.python.org/3/library/subprocess.html>`_

    :returns: The :class:`subprocess.CompletedProcess` object returned by the
              :func:`subprocess.run` function.
    :rtype: :class:`subprocess.CompletedProcess`
    """

    if (
        _log_capture is False
        or kwargs.get("stdout") is not None
        or kwargs.get("stderr") is not None
        or kwargs.get("capture_output") is True
    ):
        return subprocess.run(*args, **kwargs)
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.STDOUT
    kwargs["universal_newlines"] = True
    with subprocess.Popen(*args, **kwargs) as process:
        while process.poll() is None:
            print(process.stdout.read(1), end="", flush=True)
        else:
            print(process.stdout.read(), end="", flush=True)
            retcode = process.returncode
    return subprocess.CompletedProcess(process.args, retcode)


if __name__ == "__main__":
    pass
