
echo "" > results_pylint.txt
python -m pylint database >> results_pylint.txt
python -m pylint test_database >> results_pylint.txt
type results_pylint.txt
