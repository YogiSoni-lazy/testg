import time
from labs.ui import Step, GradingStep, run_step, run_steps
from labs.ui import print_header
from labs.activities import GuidedExercise


class ExamplePythonNewStyle(GuidedExercise):

    __LAB__ = "python-new"

    def start(self):
        print_header("Hello this is a header")

        happy_step()
        sad_step_with_exception_catching()
        grading_step()
        grading_failing_step()

        print_header("Legacy")

        run_step({
            "label": "I am a legacy item",
            "task": lambda _: None,
            "fatal": False
        })
        run_step({
            "label": "I am a legacy grading item",
            "task": lambda _: None,
            "fatal": False,
            "grading": True
        })
        run_step({
            "label": "I am a legacy item with errors",
            "task": lambda _: 1,
            "failed": True,
            "fatal": False
        })
        run_steps([
            {
                "label": "I am a legacy item",
                "task": lambda _: None,
                "fatal": False
            },
            {
                "label": "I am a legacy item with errors",
                "task": lambda _: 1,
                "failed": True,
                "fatal": False
            }
        ])

        print_header("Steps with context managers")

        happy_step_with_context()
        sad_step_with_context()
        grading_step_with_context()
        grading_failing_step_with_context()
        fatal_step()
        # This step is not going to be executed
        happy_step()

    def fix(self):
        print_header("Fixing")


# Steps...

def happy_step():
    step = Step("I am a happy step :)").start()

    # Do your thing...
    do_something()

    step.ok().end()


def sad_step_with_exception_catching():
    step = Step("I am going to fail x(", fatal=False).start()

    # Do your thing...
    try:
        step.add_message("This is risky. I might fail")
        do_something_and_fail()
    except Exception:
        step.add_error("This is an error message")
    else:
        step.ok()

    step.end()


def grading_step():
    step = GradingStep("a grading step that passes").start()

    # Some tests/grading here..
    if tests_pass():
        step.ok()
    else:
        step.add_error("This is an error message")

    step.end()


def grading_failing_step():
    step = GradingStep("a grading step that fails").start()

    # Some tests/grading here..
    if buggy_tests_pass():
        step.ok()
    else:
        step.add_error("This is an error message")

    step.end()


def happy_step_with_context():
    with Step("a happy step (context manager)") as step:

        # Do your thing...
        step.add_message("inside a context!")
        do_something()


def sad_step_with_context():
    with Step("a sad step (context manager)", fatal=False) as step:

        # Do your thing...
        try:
            do_something_and_fail()
        except Exception:
            step.add_error("something failed")


def grading_step_with_context():
    with GradingStep("a grading step that passes (context manager)") as step:
        # Some tests/grading here..
        do_something()
        if True:
            step.ok()


def grading_failing_step_with_context():
    with GradingStep("a grading step that fails (context manager)") as step:

        # Some tests/grading here..

        step.add_error("This is an error message")


def fatal_step():
    with Step("a fatal step (context manager)", fatal=True):
        do_something_and_fail()


# Misc helper functions...

def do_something():
    time.sleep(.2)


def do_something_and_fail():
    time.sleep(.2)
    raise RuntimeError("I failed on purpose")


def tests_pass():
    return True


def buggy_tests_pass():
    return False
