
echo "" > results_pylint.txt
python -m pylint linear >> results_pylint.txt
python -m pylint test_linear >> results_pylint.txt
python -m pylint parallel >> results_pylint.txt
python -m pylint test_parallel >> results_pylint.txt
type results_pylint.txt
