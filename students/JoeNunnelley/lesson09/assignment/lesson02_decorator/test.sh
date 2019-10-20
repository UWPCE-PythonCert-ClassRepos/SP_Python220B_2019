#! /usr/bin/env bash

echo 'Run Flake8'
python3 -m flake8 charges_calc.py
echo 'Run Pylint'
python3 -m pylint charges_calc.py
echo ''
echo '###############################'
echo 'Run with debug decorator active'
python3 charges_calc.py  -i source.json -o output.json -d
echo ''
echo '###############################'
echo 'Run with debug decorator inactive'
python3 charges_calc.py -i source.json -o output.json


