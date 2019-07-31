#! /usr/bin/env bash

echo 'Run Flake8'
python3 -m flake8 charges_calc.py
echo 'Run Pylint'
python3 -m pylint charges_calc.py


