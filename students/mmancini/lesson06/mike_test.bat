
echo "Poor Performance Test Results" > results_poor_performance.txt
echo "Good Performance Test Results" > results_good_performance.txt

python poor_perf.py >> results_poor_performance.txt
python good_perf.py >> results_good_performance.txt

echo off

type results_poor_performance.txt

echo on
echo ""
echo off

type results_good_performance.txt

