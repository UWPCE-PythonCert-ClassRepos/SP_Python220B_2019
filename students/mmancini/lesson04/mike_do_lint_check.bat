
echo "" > results_pylint.txt
python -m pylint basic_operations >> results_pylint.txt
python -m pylint customers_model >> results_pylint.txt
python -m pylint test_basic_operations >> results_pylint.txt
type results_pylint.txt
