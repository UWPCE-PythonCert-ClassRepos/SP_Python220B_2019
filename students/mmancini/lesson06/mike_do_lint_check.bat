
echo "" > results_pylint.txt
python -m pylint good_perf >> results_pylint.txt
type results_pylint.txt
