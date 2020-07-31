
echo "" > results_pylint.txt
python -m pylint pngdiscover >> results_pylint.txt
type results_pylint.txt
