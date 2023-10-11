import pytest
from labs import watch
from labs.watch.watchstep import is_watchstep


def test__decorator__adds_label_to_function():

    @watch.watchstep("12345")
    def dummy():
        pass

    assert dummy.label == "12345"


def test__expect__doesnt_raise_testerror():
    watch.expect(True)


def test__expect__raises_testerror():
    with pytest.raises(watch.LabWatchStepFailure):
        watch.expect(False)


def test__istest__returns_true_if_function_is_decorated():

    @watch.watchstep("12345")
    def dummy():
        pass

    assert is_watchstep(dummy)


def test__istest__returns_false():

    def dummy():
        pass

    assert not is_watchstep(dummy)


def test__checkerror__has_error():
    error = watch.LabWatchStepFailure("Error", ["Do xyz"])
    assert error.message == "Error"


def test__checkerror__has_hints():
    error = watch.LabWatchStepFailure("Error", ["Do xyz"])
    assert error.hints == ["Do xyz"]
