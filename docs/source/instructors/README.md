# Tips for Instructors and Students

Instructors and students might find this information useful is something goes wrong.

## Inspecting the Logs

To inspect the logs produced by a lab script.

1. Find the log directory in the DynoLabs configuration file

```console
[student@workstation ~]$ cat ~/.grading/config.yaml
rhtlab:
  course:
    sku: do378
  logging:
    level: error
    path: /tmp/log/labs
```

2. Navigate to the logging path. You might find several files, one per exercise:

```console
[student@workstation ~]$ cd /tmp/log/labs
[student@workstation labs]$ ls
start_setup
```

3. Inspect the contents of the file that corresponds to the problematic exercise.

## Adjusting the Log Level

Lab scripts might produce more information if you lower the log level, which by default is `error`.

To change the level, edit the `~/.grading/config.yaml` file, and set the `rhtlab.logging.level` property.
For example, you might want to change the level to `debug`:

```console
rhtlab:
  course:
    sku: do378
  logging:
    level: debug
    path: /tmp/log/labs
```


## Introspecting the Lab Scripts Code

In most classroom environments, lab scripts are installed in the `~/.venv/labs/` virtual environent.
As a result:

* `python` points to `~/.venv/labs/bin/python`
* The source code of `rht-labs-core` is available at `~/.venv/labs/bin/python3.6/site-packages/labs`.
* The source code of the course package (`rht-labs-<sku>`) is available at `~/.venv/labs/bin/python3.6/site-packages/<sku>`.

:::{caution}
Modifying the lab script source code can be useful to fix small issues, but it can lead to unexpected consequences.

If you break the code, you can use `pip` or `lab install` to re-install the original package.
:::