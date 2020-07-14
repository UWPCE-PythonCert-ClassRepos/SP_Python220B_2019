
python -m unittest test_linear.py > results_linear.txt 2>&1

echo "linear runtime:" >> results_linear.txt
python linear.py >> results_linear.txt 2>&1
type results_linear.txt

