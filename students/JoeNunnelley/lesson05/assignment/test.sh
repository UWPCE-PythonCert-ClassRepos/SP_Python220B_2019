#! /usr/bin/env bash

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint database.py --rcfile=pylintrc
echo 'FLAKE8 EXAMINATION'
python3 -m flake8 .
#echo 'COVERAGE RUN'
#python3 -m coverage run --source= -m unittest tests/test_unit.py tests/test_integration.py
#echo 'COVERAGE REPORT'
#python3 -m coverage report
#echo 'COVERAGE HTML REPORT'
#python3 -m coverage html
echo 'DONE'
