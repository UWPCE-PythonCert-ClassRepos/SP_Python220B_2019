#! /usr/bin/env bash

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint linear.py --rcfile=pylintrc
echo 'FLAKE8 EXAMINATION'
python3 -m flake8 linear.py 
echo 'RUN CODE'
python3 linear.py
echo 'DONE'
