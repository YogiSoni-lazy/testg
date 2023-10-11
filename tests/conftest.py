import os
import logging
from pathlib import Path


def pytest_configure():
    # We should not pollute the dev enviroment,
    # so let's use a different config file for tests
    config_path = str(
        Path(__file__).parent.joinpath("_util").joinpath("config.yaml")
    )

    os.environ["RHT_LABS_CONFIG_PATH"] = config_path

    logging.info(f"DynoLabs config path: {config_path}")
