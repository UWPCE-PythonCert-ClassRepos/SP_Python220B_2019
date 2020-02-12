## Initial analysis of poor_perf.py
With 1,000,000 records, analyze() took 4.204673 seconds:
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
