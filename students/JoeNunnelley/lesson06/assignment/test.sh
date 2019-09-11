#! /usr/bin/env bash

FILE='good_perf.py'

echo "PYLINT EXAMINATION [$FILE]"
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint $FILE --rcfile=pylintrc
echo "FLAKE8 EXAMINATION OF [$FILE]"
python3 -m flake8 $FILE
echo "RUN CODE [$FILE]"
python3 $FILE
echo 'DONE'
