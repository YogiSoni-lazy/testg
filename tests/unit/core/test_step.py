
from labs.core.step import step


def test_labstep():
    """
    A lab step can be treated as an object
    """
    item = {
        "label": "Test step",
        "task": dummy
    }

    labstep = step(item)

    assert labstep.label == "Test step"
    assert labstep.task == dummy


def test_labstep_header_only():
    """
    A lab step can be initialized as a header-only step
    """
    item = {
        "header": "Hello"
    }

    labstep = step(item)

    assert labstep.header == "Hello"


def test_labstep_failure():
    """
    Mark a lab step as failed
    """
    item = {
        "label": "Test step",
        "task": dummy
    }

    labstep = step(item)
    labstep.fail()

    assert labstep.failed


def test_labstep_messages():
    """
    Labstep can add messages
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "msgs": [{"text": "hello"}]
    }

    labstep = step(item)
    labstep.add_message("Hey")

    assert labstep.msgs == [{"text": "hello"}, {"text": "Hey"}]


def test_labstep_message_texts():
    """
    Labstep can return a list of message texts
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "msgs": [{"text": "hello"}, {"no": "text"}]
    }

    labstep = step(item)
    labstep.add_message("Hey")

    assert labstep.get_text_messages() == ["hello", "Hey"]


def test_labstep_task_grading():
    """
    Check if a step is for grading
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "grading": True
    }

    labstep = step(item)

    assert labstep.grading


def test_labstep_task_fatal():
    """
    Check if a step is fatal
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "fatal": True
    }

    labstep = step(item)

    assert labstep.fatal


def test_condition():
    """
    Labstep accepts a condition predicate
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "condition": lambda x: x == "is true",
        "my_parameter": 1234
    }

    labstep = step(item)

    assert labstep.condition("is true")


def test__default_condition():
    """
    Labstep sets a default condition function to be True
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "my_parameter": 1234
    }

    labstep = step(item)

    assert labstep.condition()


def test__grading_is_false_by_default():
    """
    Labstep set the grading flag to False, by default
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "my_parameter": 1234
    }

    labstep = step(item)

    assert not labstep.grading


def test__header():
    """
    Labstep set the grading flag to False, by default
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "header": "Hello"
    }

    labstep = step(item)

    assert labstep.header == "Hello"


def test__header_is_none_by_default():
    """
    Labstep set the grading flag to False, by default
    """
    item = {
        "label": "Test step",
        "task": dummy,
    }

    labstep = step(item)

    assert labstep.header is None


def test_additional_parameters():
    """
    Labstep supports additional properties
    You can access additional properties with the dict-like notation
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "my_parameter": 1234
    }

    labstep = step(item)

    assert labstep.my_parameter == 1234


# Dict versions


def test_labstep_as_dict():
    """
    A lab step can be created and read as a dict
    """
    item = {
        "label": "Test step",
        "task": dummy
    }

    labstep = step(item)

    assert labstep["label"] == "Test step"
    assert labstep["task"] == dummy


def test_labstep_can_use_get_method():
    """
    A lab step can be created and read as a dict
    """
    item = {
        "label": "Test step",
        "task": dummy
    }

    labstep = step(item)

    assert labstep.get("label") == "Test step"


def test_labstep_failure_dict():
    """
    Mark a lab step as failed (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy
    }

    labstep = step(item)
    labstep["failed"] = True

    assert labstep["failed"]


def test_labstep_task_grading_dict():
    """
    Check if a step is for grading (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "grading": True
    }

    labstep = step(item)

    assert labstep["grading"]


def test_labstep_messages_dict():
    """
    Labstep can add messages (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "msgs": [{"text": "hello"}]
    }

    labstep = step(item)
    labstep["msgs"].append({"text": "Hey"})

    assert labstep["msgs"] == [{"text": "hello"}, {"text": "Hey"}]


def test_labstep_task_fatal_dict():
    """
    Check if a step is fatal (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "fatal": True
    }

    labstep = step(item)

    assert labstep["fatal"]


def test_labstep_task_failed_dict():
    """
    Check if a step failed (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "failed": True,
        "fatal": True
    }

    labstep = step(item)

    assert labstep["failed"]


def test_additional_parameters_dict():
    """
    Labstep supports additional kwargs (dict version)
    """
    item = {
        "label": "Test step",
        "task": dummy,
        "my_parameter": 1234
    }

    labstep = step(item)

    assert labstep["my_parameter"] == 1234


def dummy():
    pass
