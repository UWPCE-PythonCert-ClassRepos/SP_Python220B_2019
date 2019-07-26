#! /usr/bin/env bash

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}/calculator"
python3 -m pylint ./calculator --rcfile=./calculator/pylintrc
echo 'COVERAGE RUN'
python3 -m coverage run --source=calculator -m unittest test_unit.py test_integration.py
echo 'COVERAGE REPORT'
python3 -m coverage report
echo 'COVERAGE HTML REPORT'
python3 -m coverage html
echo 'DONE'
