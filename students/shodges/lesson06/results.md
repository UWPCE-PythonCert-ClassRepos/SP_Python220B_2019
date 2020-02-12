## Analysis Overview
| Timing Method  | [Baseline](#poor_perfpy) | [Change 1](#good_perf_1py) | [Change 2](#good_perf_2py) | [Change 3](#good_perf_3py) |
| -------------- | ------------------------ | -------------------------- | -------------------------- | -------------------------- |
| Timestamp diff | 4.204673                 | 2.432901                   | 2.123108                   | 1.662266                   |
| time -p        | 4.12                     | 2.70                       | 2.16                       | 1.73                       |
## poor_perf.py
These tests establish the baseline utilizing the following analyze() function:

With 1,000,000 records, analyze() took 4.204673 seconds according to the difference in timestamps and 4.12 seconds according to time.
```
>>> import poor_perf
>>> poor_results = poor_perf.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
>>> poor_results
(datetime.datetime(2020, 2, 12, 10, 11, 10, 531725), datetime.datetime(2020, 2, 12, 10, 11, 14, 736398), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}, 500161)
>>> poor_results[1] - poor_results[0]
datetime.timedelta(seconds=4, microseconds=204673)
```
```
shodges-ltm:lesson06 shodges$ time -p python3 poor_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 4.12
user 4.00
sys 0.10
```

## good_perf_1.py
I removed the for loop that processed the CSV a second time and moved its analysis into the primary for loop.

With this change, the timestamp diff shows 2.432901 seconds and time shows a runtime of 2.70 seconds.
```
>>> import good_perf_1
>>> good_results_1 = good_perf_1.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
>>> good_results_1
(datetime.datetime(2020, 2, 12, 14, 37, 6, 418506), datetime.datetime(2020, 2, 12, 14, 37, 8, 851407), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}, 500161)
datetime.timedelta(seconds=2, microseconds=432901)
```
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf_1.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 2.70
user 2.60
sys 0.08
```

## good_perf_2.py
I removed the usage of new_ones (and the secondary processing for loop) and moved the date analysis to the primary for loop.

Timestamp diffs now show a runtime of 2.123108 seconds and time shows a runtime of 2.16 seconds.
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf_2.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 2.16
user 2.12
sys 0.02
```
```
>>> import good_perf_2
>>> good_results_2 = good_perf_2.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
>>> good_results_2
(datetime.datetime(2020, 2, 12, 14, 38, 31, 426815), datetime.datetime(2020, 2, 12, 14, 38, 33, 549923), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}, 500161)
>>> good_results_2[1] - good_results_2[0]
datetime.timedelta(seconds=2, microseconds=123108)
```

## good_perf change 3
Rather than the successive conditionals for the year analysis, I changed it to directly leverage the year as the key.  We'll of course need to catch a KeyError here in case we have years in the dataset that we're not interested in counting (which we do).

We now get runtimes of 1.662266 seconds and 1.73 seconds.
```
>>> import good_perf_3
>>> good_results_3 = good_perf_3.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
>>> good_results_3
(datetime.datetime(2020, 2, 12, 14, 45, 6, 943589), datetime.datetime(2020, 2, 12, 14, 45, 8, 605855), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}, 500161)
>>> good_results_3[1] - good_results_3[0]
datetime.timedelta(seconds=1, microseconds=662266)
```
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf_3.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
real 1.73
user 1.69
sys 0.02
```
