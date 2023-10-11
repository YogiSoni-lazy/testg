# Implementing Lab Scripts

To write a lab script:

1. Subclass the {py:class}`labs.activities.GuidedExercise` or {py:class}`labs.activities.Lab` classes.
    * These classes are aliases, so the difference between them is merely semantic.
2. Define the lab script name in the `__LAB__` class property.
    * Dynolabs uses this value to locate the lab scripts.
    * For example, when you run `lab start install-setup`, Dynolabs uses the class with `__LAB__==install-setup`.
1. Implement the `start` and `finish` methods.
2. If the exercise requires grading, implement the `grade` method.
3. If the exercise requires autofix or autosolve logic, implement the `fix` method.

For example:

```python
from labs.activities import GuidedExercise


class InstallSetup(GuidedExercise):
    __LAB__ = "install-setup"

    def start(self):
        ...

    def grade(self):
        ...

    def fix(self):
        ...

    def finish(self):
        ...
```

Each method should execute a series of steps.
A *step* is an object that executes an action and displays the result in the console.
You can create steps with the {py:class}`labs.ui.Step` class.

Examples are available at `packages-gl006/src/gl006/example-python-new-style.py`.

:::{warning}
This section is in progress...
:::