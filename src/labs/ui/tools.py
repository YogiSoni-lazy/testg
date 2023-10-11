from click import echo, secho, style


def print_header(message: str):
    echo()
    secho(message, bold=True)
    echo()


def print_start_header():
    print_lab_header("Starting")


def print_finish_header():
    print_lab_header("Finishing")


def print_grade_header():
    print_lab_header("Grading")


def print_lab_header(action: str):
    print_header(f"{action} lab...")


def format_message(message: str, left_padding="", bullet="", color=None):
    return left_padding + bullet + style(message, fg=color)
