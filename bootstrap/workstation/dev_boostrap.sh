#!/bin/bash

# Setup the development environment for dynolabs

LABS_CORE_DIR="${HOME}/rht-labs-core"

cd $LABS_CORE_DIR
echo "Boostrapping Dynolabs on workstation for development"
sudo dnf install -y make
sudo alternatives --set python /usr/bin/python3
make venv
source ~/.venv/labs/bin/activate
pip install --editable .
