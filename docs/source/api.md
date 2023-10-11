# DynoLabs API

This section of the documentation covers all the common interfaces of the DynoLabs Core.

:::{attention}
Work in Progress!!
:::

## `labs`

The root module exported by `rht-labs-core`.

## `labs.activites`

High-level abstract classes that represent lab scripts.
Extend `GuidedExercise` or `Lab` classes and implement the `start`, `finish` and `grade` actions of a particular activity.

For example:

```python
from labs.activities import GuidedExercise

class MonitorTrace(GuidedExercise):

    __LAB__ = "monitor-trace"

    def start(self):
        ...

    def finish(self):
        ...
```


```{eval-rst}
.. automodule:: labs.activities
    :members:
    :inherited-members:
```



## `labs.ui`

Use this module to define steps in your lab scripts.

```{eval-rst}
.. automodule:: labs.ui
    :members:
    :inherited-members:
    :undoc-members:
```

## `labs.ui.steps.ansible`

Use this module to run Ansible in your lab scripts.

```{eval-rst}
.. automodule:: labs.ui.steps.ansible
    :members:
    :inherited-members:
    :undoc-members:
```

## `labs.watch`

Tools to watch labs for changes

```{eval-rst}
.. automodule:: labs.watch
    :members:
```


## `labs.common.commands`

```{eval-rst}
.. automodule:: labs.common.commands
    :members:
```

## `labs.common.containers`

```{eval-rst}
.. automodule:: labs.common.containers
    :members:
```

## `labs.common.fs`

```{eval-rst}
.. automodule:: labs.common.fs
    :members:
```

## `labs.common.http`

```{eval-rst}
.. automodule:: labs.common.http
    :members:
```

## `labs.common.playbooks`

```{eval-rst}
.. automodule:: labs.common.playbooks
    :members:
```

## `labs.common.git.repository`

Tools to manage GIT repositories.

```{eval-rst}
.. automodule:: labs.common.git.repository
    :members:
    :undoc-members:
```

## `labs.common.workspace`

Tools to create and manage working directories and configuration files for courses.

```{eval-rst}
.. automodule:: labs.common.workspace
    :members:
```
## `labs.common.config`

Tools to read and write course configuration files.

```{eval-rst}
.. automodule:: labs.common.config
    :members:
```

## `labs.common.utils`

```{eval-rst}
.. automodule:: labs.common.utils
    :members:
```
