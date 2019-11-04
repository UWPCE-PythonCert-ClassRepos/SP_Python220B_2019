#! /usr/bin/env bash

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint database.py --rcfile=pylintrc
echo 'FLAKE8 EXAMINATION'
python3 -m flake8 .
echo 'RUN CODE'
python3 database.py
