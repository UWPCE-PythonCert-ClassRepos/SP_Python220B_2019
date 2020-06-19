python -m coverage run -m unittest test_basic_operations.py > results_coverage.txt
python -m coverage report >> results_coverage.txt
type results_coverage.txt
