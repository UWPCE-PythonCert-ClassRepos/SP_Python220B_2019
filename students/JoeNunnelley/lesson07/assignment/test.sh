#! /usr/bin/env bash

FILE=$1

echo 'PYLINT EXAMINATION'
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint $FILE --rcfile=pylintrc
echo 'FLAKE8 EXAMINATION'
python3 -m flake8 $FILE 
echo 'RUN CODE'
python3 $FILE
echo 'DONE'
