import os
import requests
from src.labs.version import __version__


PACKAGE = "rht-labs-core"
PYPI_STAGE = "https://pypi.apps.tools.dev.nextcle.com/repository/labs"
PIPI_PROD = "https://pypi.apps.tools-na.prod.nextcle.com/repository/labs"


def get_pypi_url():
    stage_mode = os.getenv("STAGE", "False").lower() in ("true", "1", "t")
    return PYPI_STAGE if stage_mode else PIPI_PROD


if __name__ == "__main__":
    pypi = get_pypi_url()
    version = os.environ.get("VERSION", __version__)

    url = f"{pypi}/packages/{PACKAGE}/{version}/{PACKAGE}-{version}.tar.gz"
    print("Check package URL: ", url)
    response = requests.head(url)

    if response.status_code == 200:
        print(f"{PACKAGE} {version} exists in {pypi}")
    else:
        print(f"{PACKAGE} {version} not found in {pypi}")
        exit(1)
