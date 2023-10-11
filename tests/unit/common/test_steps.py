from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from labs.common import steps
from labs.common.userinterface import Console
from labs.laberrors import LabError
from labs.ui.step import StepFatalError


def test__copy_lab_files__copies_dir():
    """
    copy_lab_files copies a directory to a given destination
    """
    with TemporaryDirectory() as source:
        with TemporaryDirectory() as destination:
            destination_path = Path(destination).joinpath("my-lab")

            step = steps.copy_lab_files(fromdir=source, to=destination_path)

            run(step)

            assert destination_path.is_dir()


def test__copy_lab_files__dirs_do_not_exist():
    """
    copy_lab_files fails by default if dirs do not exist
    """
    step = steps.copy_lab_files(fromdir="i/do/not/exist", to="___")

    with pytest.raises(LabError):
        run(step)

    assert step.failed


def test__copy_lab_files__dirs_do_not_exist__ignore():
    """
    copy_lab_files ignores non-existing source dirs
    if "no_source_error" is False
    """
    step = steps.copy_lab_files(
        fromdir="i/do/not/exist", to="___", no_source_error=False
    )

    run(step)

    assert not step.failed


def test__copy_lab_files__label():
    """
    copy_lab_files can have a different label
    """
    step = steps.copy_lab_files(label="Hello", fromdir="a", to="b")

    assert step.label == "Hello"


def test__copy_materials_step__copies_dir():
    """
    copy_materials copies a directory to a given destination
    """
    with TemporaryDirectory() as source:
        with TemporaryDirectory() as destination:
            lab_name = "test-lab"
            destination_path = Path(destination)
            source_path = Path(source)
            materials_path = _prepare_valid_source_tree(lab_name, source_path)

            step = steps.copy_materials_step(
                materials_path=materials_path,
                lab_name=lab_name, to=destination_path
            )

            destination_labs_path = destination_path / "labs" / lab_name
            destination_solutions_path = (destination_path /
                                          "solutions" / lab_name)
            assert step.has_succeeded()
            assert destination_labs_path.exists()
            assert destination_solutions_path.exists()


def test__copy_materials_step__dest_dir_not_empty_warns(monkeypatch):
    """
    copy_materials warns with an existing SKU/labs/lab-name/any_content
    destination and no overwrite
    """
    monkeypatch.setenv("OVERWRITE", "False")
    with TemporaryDirectory() as source:
        with TemporaryDirectory() as destination:
            lab_name = "test-lab"
            destination_path = Path(destination)
            materials_path = _prepare_valid_source_tree(lab_name, Path(source))
            target_lab = destination_path / "labs" / lab_name
            target_lab_content = target_lab / "any_content"
            target_lab_content.mkdir(parents=True)

            step = steps.copy_materials_step(
                    materials_path=materials_path,
                    lab_name=lab_name,
                    to=destination_path)

            assert step.has_succeeded()
            assert target_lab_content.exists()
            assert f"Path {target_lab} not empty... Execute OVERWRITE=true" \
                   " lab start ... to overwrite the files" \
                   in step.secondary_messages


def test__copy_materials_step__dest_dir_not_empty_success(monkeypatch):
    """
    copy_materials overwrites a directory to a given non-empty destination
    """
    monkeypatch.setenv("OVERWRITE", "true")
    with TemporaryDirectory() as source:
        with TemporaryDirectory() as destination:
            lab_name = "test-lab"
            destination_path = Path(destination)
            materials_path = _prepare_valid_source_tree(lab_name, Path(source))
            destination_labs_path = destination_path / "labs" / lab_name
            overwritten_path = destination_labs_path / "will_be_overwritten"
            overwritten_path.mkdir(parents=True)

            step = steps.copy_materials_step(
                materials_path=materials_path,
                lab_name=lab_name,
                to=destination_path)

            destination_solutions_path = (destination_path /
                                          "solutions" / lab_name)
            assert step.has_succeeded()
            assert destination_labs_path.exists()
            assert destination_solutions_path.exists()
            assert not overwritten_path.exists()


def test__copy_materials_step__course_dir_not_empty_success():
    """
    copy_materials works with an existing SKU/labs destination
    """
    with TemporaryDirectory() as source:
        with TemporaryDirectory() as destination:
            lab_name = "test-lab"
            destination_path = Path(destination)
            materials_path = _prepare_valid_source_tree(lab_name, Path(source))
            destination_labs_path = destination_path / "labs"
            destination_labs_path.mkdir(parents=True)

            step = steps.copy_materials_step(
                materials_path=materials_path,
                lab_name=lab_name,
                to=destination_path)

            destination_solutions_path = (destination_path /
                                          "solutions" / lab_name)

            assert step.has_succeeded()
            assert (destination_labs_path / lab_name).exists()
            assert destination_solutions_path.exists()


def test__copy_materials_step__dirs_do_not_exist():
    """
    copy_lab_files fails by default if source dir not exists
    """
    with pytest.raises(StepFatalError) as ex:
        steps.copy_materials_step(
            materials_path=Path("i/do/not/exist"),
            lab_name="test-lab",
            to=Path("___")
        )

    assert ex.value.step.has_failed()
    assert "i/do/not/exist is not a directory or does not exist. " \
           in ex.value.step.secondary_messages[0]


# Utils

def run(step):
    Console([step]).run_items()


def _prepare_valid_source_tree(lab_name, source_path):
    materials_path = source_path / "materials"
    materials_path.mkdir()
    materials_lab_path = materials_path / "labs" / lab_name / "lab-content"
    materials_lab_path.mkdir(parents=True)
    solutions_lab_path = materials_path / "solutions" / lab_name
    solutions_lab_path.mkdir(parents=True)
    return materials_path
