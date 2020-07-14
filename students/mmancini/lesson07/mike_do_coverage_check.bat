python -m coverage run -m unittest test_linear.py > results_linear_coverage.txt
python -m coverage report >> results_linear_coverage.txt
python -m coverage run -m unittest test_parallel.py > results_parallel_coverage.txt
python -m coverage report >> results_parallel_coverage.txt
type results_linear_coverage.txt
type results_parallel_coverage.txt
