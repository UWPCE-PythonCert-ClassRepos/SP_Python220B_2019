
echo "" > results_pylint.txt
python -m pylint inventory >> results_pylint.txt
python -m pylint test_inventory >> results_pylint.txt
type results_pylint.txt
