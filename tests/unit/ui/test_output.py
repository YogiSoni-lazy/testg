from io import StringIO
from labs.ui import Step


def test__step__prints_label():
    step, out = create_step_with_out_stream("hello")

    step.start()

    assert "hello" in out.getvalue()


def test__step__prints__success():
    step, out = create_step_with_out_stream("hello")

    step.start()
    step.ok().end()
    assert "SUCCESS" in out.getvalue()


def test__step__prints__failure():
    step, out = create_step_with_out_stream("hello")

    step.start()
    step.add_error("something is failing").end()
    assert "FAIL" in out.getvalue()


def test__grading_step__prints__pass():
    step, out = create_step_with_out_stream("hello", grading=True)

    step.start()
    step.ok().end()
    assert "PASS" in out.getvalue()


def create_step_with_out_stream(label, grading=False):
    out = StringIO()

    step = Step(label, fatal=False, grading=grading)
    step._spinner._stream = out
    return step, out
