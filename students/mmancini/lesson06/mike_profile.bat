

echo "Poor Profile Results" > results_poor_profile.txt
echo "Good Profile Results" > results_good_profile.txt

python -m cProfile poor_perf.py >> results_poor_profile.txt
python -m cProfile good_perf.py >> results_good_profile.txt

echo off

type results_poor_profile.txt

echo on
echo ""
echo off

type results_good_profile.txt

