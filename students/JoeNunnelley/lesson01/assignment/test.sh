#! /usr/bin/env bash

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}/inventory_management"
python3 -m pylint ./inventory_management/ --rcfile=./inventory_management/pylintrc
echo 'COVERAGE RUN'
python3 -m coverage run --source=inventory_management -m unittest test_unit.py test_integration.py
echo 'COVERAGE REPORT'
python3 -m coverage report
echo 'COVERAGE HTML REPORT'
python3 -m coverage html
echo 'DONE'
