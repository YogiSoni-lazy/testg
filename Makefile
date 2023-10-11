#!/usr/bin/make -f
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#
# You MUST define the PS_PASSWD variable before running that Makefile.
# The variable must be set with the password of the PyPI server.
#
# - Tasks executed with `python3` are meant to be run from outside the venv
# - Tasks executed with `python`  are meant to be run from inside  the venv

SHELL=/bin/bash

PYPI_USER=pypi
PYPI_SERVER_DEV=https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/
PYPI_SERVER_PROD=https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/

DIST_FILES=dist/$(shell ls -1A dist)

# This is the standard venv location on the workstation machine
VENV=~/.venv/labs
PIP_LOG=pip-log.txt

default: build

# Create virtual environment and install all requirements
# We use '&&' to run *all commands* in a single subshell
# Redirect all pip output to ${PIP_LOG} (ignored by git)
venv:	requirements.txt
	python3 -m venv ${VENV} && \
	source ${VENV}/bin/activate && \
	  pip3 install --upgrade pip > ${PIP_LOG} && \
	  pip3 install -r requirements.txt >> ${PIP_LOG} && \
	deactivate
	@echo ""
	@echo "All done, execute 'source ${VENV}/bin/activate' to enter the venv"
	@echo ""

clean:
	-rm -rf dist build .eggs *.egg-info ${PIP_LOG}

# Abort if the user is currently "inside" the Python virtual environment
distclean:     clean
ifneq (,$(shell pip3 -V | grep '${USER}'))
	$(error You are inside the venv, please run "deactivate" and try again)
endif
	-rm -rf ${VENV}

lint:
	python -m flake8

test-unit:
	python -m pytest -x tests/unit

test-integration:
	python -m pytest -x tests/integration

test:
	python -m pytest -x

build: clean
	python3 setup.py sdist

build-dev: clean
	python setup.py egg_info --tag-build=$(DEV_VERSION) sdist

publish-stage:
ifdef PS_PASSWD
	@twine upload --verbose --repository-url ${PYPI_SERVER_DEV} -u ${PYPI_USER} -p "$$PS_PASSWD" ${DIST_FILES}
else
	$(error The PS_PASSWD environment variable is not set. Please set it with the password of the stage PyPI server.)
endif

publish-prod:
ifdef PS_PASSWD_PROD
	@twine upload --verbose --repository-url ${PYPI_SERVER_PROD} -u ${PYPI_USER} -p $(PS_PASSWD_PROD) ${DIST_FILES}
else
	$(error The PS_PASSWD_PROD environment variable is not set. Please set it with the password of the production PyPI server.)
endif
