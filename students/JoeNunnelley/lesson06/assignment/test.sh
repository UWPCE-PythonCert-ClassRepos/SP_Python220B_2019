#! /usr/bin/env bash

echo "PYLINT EXAMINATION [$1]"
export PYTHONPATH=$PYTHONPATH:"${PWD}"
python3 -m pylint $1 --rcfile=pylintrc
echo "FLAKE8 EXAMINATION OF [$1]"
python3 -m flake8 .
echo "RUN CODE [$1]"
python3 $1 
echo 'DONE'
