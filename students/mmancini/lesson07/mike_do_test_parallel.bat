
python -m unittest test_parallel.py > results_parallel.txt 2>&1
type results_parallel.txt


echo "parallel runtime:" >> results_parallel.txt
python parallel.py >> results_parallel.txt 2>&1
type results_parallel.txt

