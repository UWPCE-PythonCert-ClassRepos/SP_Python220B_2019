python -m coverage run --source=inventory_management -m unittest test_unit.py > results_coverage.txt
python -m coverage report >> results_coverage.txt
type results_coverage.txt
