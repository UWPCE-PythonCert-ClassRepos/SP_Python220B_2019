## Analysis Overview
| Timing Method  | [Baseline](#poor_perfpy) | [Change 1](#good_perf_1py) | [Change 2](#good_perf_2py) | [Change 3](#good_perf_3py) | [Change 4](#good_perf_4py) |
| -------------- | ------------------------ | -------------------------- | -------------------------- | -------------------------- | -------------------------- |
| Timestamp diff | 4.204673                 | 2.432901                   | 2.123108                   | 1.662266                   | 1.747035                   |
| time -p        | 4.12                     | 2.70                       | 2.16                       | 1.73                       | 1.79                       |
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

## good_perf_3.py
Rather than the successive conditionals for the year analysis, I changed it to directly leverage the year as the key.  We'll of course need to catch a KeyError here in case we have years in the dataset that we're not interested in counting (which we do).

This also revealed a logic flaw in the original code:
```python
    if new[0][6:] == '2018':
        year_count["2017"] += 1
```
Now that we're properly recording 2018 (and by extension, 2017) counts, the results will look a bit different.  The corrected results from poor_perf.py are: ```{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}```

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

## good_perf_4.py
This time I removed the conditional looking for 'ao' and add the integer representation of the boolean response of ```'ao' in row[6]``` to ```found```.

We now get runtimes of 1.747035 seconds and 1.79 seconds.  We've actually made the runtime a bit worse.
```
>>> import good_perf_4
>>> good_results_4 = good_perf_4.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
>>> good_results_4
(datetime.datetime(2020, 2, 12, 14, 58, 33, 452492), datetime.datetime(2020, 2, 12, 14, 58, 35, 199527), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}, 500161)
>>> good_results_4[1] - good_results_4[0]
datetime.timedelta(seconds=1, microseconds=747035)
```
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf_4.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
real 1.79
user 1.75
sys 0.02
```

## Final results
[Change 3](#good_perf_3py) resulted in a much more optimized version of [poor_perf.py](#poor_perfpy).  [Further changes](#good_perf_4py) resulted in slight increases in code runtime at the cost of decreased code readability.  As shown in the analysis block, the input and output are identical to poor_perf.py (after I corrected the logic error), so the core functionality of the analysis remained the same -- just faster!

However, to ensure the output is the same as the original, the final submission has two copies with aligned outputs:
poor_perf.py and good_perf.py (where the logic error is preserved in poor_perf.py and accounted for in good_perf.py)

```
shodges-ltm:lesson06 shodges$ time -p python3 poor_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 4.04
user 3.93
sys 0.10
shodges-ltm:lesson06 shodges$ time -p python3 good_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 1.85
user 1.82
sys 0.02
```
and poor_perf_corrected.py and good_perf_corrected.py (where the logic error is corrected in poor_perf.py and good_perf.py utilizes change 3 without a workaround)
```
shodges-ltm:lesson06 shodges$ time -p python3 poor_perf_corrected.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
real 4.08
user 3.97
sys 0.09
shodges-ltm:lesson06 shodges$ time -p python3 good_perf_corrected.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 99778, '2018': 99853}
'ao' was found 500161 times
real 1.76
user 1.72
sys 0.02
```

As shown, there is a slight time penalty for working around the error, but we want to make sure that the data is output as expected.  Whether intended or not, the counting of data with a year of 2018 as 2017 is expected, so we want to ensure we're comparing like for like.
