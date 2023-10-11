from setuptools import setup
import src.labs.version as ver


setup(
    include_package_data=True,
    version=ver.__version__
)
