#!/bin/sh

virtualenv -p python3 ../venv
source ../venv/bin/activate
pip install -r rnt/requirements.txt
