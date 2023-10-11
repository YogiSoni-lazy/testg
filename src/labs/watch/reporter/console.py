"""
Console output functions to show lab progress
"""
from datetime import datetime
import click
from .base import WatchReporter
from ..watchstep import LabWatchStepFailure
from ..round import WatchRoundResults


class ConsoleWatchReporter(WatchReporter):
    """
    A lab watch reporter that echoes the output to the console
    """

    headermsg: str

    def __init__(self, headermsg: str) -> None:
        self.headermsg = headermsg
        super().__init__()

    def report(self, results: WatchRoundResults):
        # Do not clear screen to allow the user
        # to scroll up and see previous output
        #  console.clear()

        echo_header(self.headermsg)

        for i, item in enumerate(results.items, start=1):
            echo_step(item.description, i, item.error)

        echo_footer(results.passing, results.failing)

    def success(self):
        click.echo("")
        click.secho(
            "You have successfully completed the exercise.",
            fg="green", bold=True
        )

    def finish(self):
        command = click.style("lab finish", fg="bright_white", bold=True)
        warning = click.style("this will clean up resources", fg="yellow")
        click.echo(
            f"Would you like to run '{command}' (default: y) ?"
            f" ({warning}) [y|n]",
            nl=False
        )
        c = click.getchar().lower()

        click.echo()

        if c == "n" or c == "no":
            return False

        return True


def clear():
    click.clear()


def echo_header(labname=""):
    now = datetime.now().strftime("%H:%M:%S")
    header = f"🔎 [{now}] {labname}"
    click.echo("")
    click.echo("")
    click.echo(header)
    click.echo("")
    click.echo("")


def echo_step(
    description: str,
    number: int,
    error: LabWatchStepFailure = None
):
    if error:
        echo_failing_step(description, number, error)
    else:
        echo_passing_step(description, number)

    click.echo("")


def echo_passing_step(description: str, number: int):
    checkmark = click.style("✓", fg="green")
    description = click.style(description, bold=True, fg="bright_white")
    click.echo(f"{checkmark} {number}. {description}")


def echo_failing_step(
    description: str,
    number: int,
    error: LabWatchStepFailure
):
    errormark = click.style("✖", fg="red")
    hintmark = click.style("Hint", fg="cyan")
    description = click.style(description, bold=True, fg="bright_white")
    click.echo(f"{errormark} {number}. {description}", err=True)
    click.secho(f"  {error.message}", fg="red", err=True)
    for hint in error.hints:
        click.secho(f"  {hintmark}: {hint}", err=True)


def echo_footer(passing: int, failing: int):
    click.secho(f"{passing} passing", fg="green")
    click.secho(f"{failing} failing", fg="red")
