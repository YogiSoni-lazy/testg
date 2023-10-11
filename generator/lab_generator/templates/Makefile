#!/usr/bin/make -f
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.
#
# You MUST define the PS_PASSWD variable before running that Makefile.
# The variable must be set with the password of the PyPI server.

SHELL=/bin/bash

PYPI_USER=pypi
PYPI_SERVER_DEV=https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/
PYPI_SERVER_PROD=https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/

DIST_FILES=dist/$(shell ls -1A dist)

default: build

clean:
	-rm -rf dist build .eggs

lint:
	flake8 .

test:
    # this step will fail if your source code does not have tests.
	# consider adding tests, or replacing this with just invoking "true"
	python3 -m pytest

build: clean
	python3 setup.py sdist

build-dev: clean
	python3 setup.py egg_info --tag-build=.dev$(BUILD_ID) sdist

publish-stage: clean build
ifdef PS_PASSWD
	@twine upload --verbose --repository-url ${PYPI_SERVER_DEV} -u ${PYPI_USER} -p "$$PS_PASSWD" ${DIST_FILES}
else
	$(error The PS_PASSWD environment variable is not set. Please set it with the password of the stage PyPI server.)
endif

publish-prod: clean build
ifdef PS_PASSWD_PROD
	@twine upload --verbose --repository-url ${PYPI_SERVER_PROD} -u ${PYPI_USER} -p "$$PS_PASSWD_PROD" ${DIST_FILES}
else
	$(error The PS_PASSWD_PROD environment variable is not set. Please set it with the password of the production PyPI server.)
endif
