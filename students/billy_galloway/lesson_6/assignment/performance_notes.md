# Performance and Profiling
After correcting the issues to get the code to run in `poor_perf.py` actually ran faster than my first `good_perf.py` version.

### python poor_perf.py  
```
{'2013': 167220, '2014': 166706, '2015': 166962, '2016': 166514, '2017': 166894, '2018': 165704}
'ao' was found 116900 times
(datetime.datetime(2020, 3, 10, 19, 4, 48, 70532), datetime.datetime(2020, 3, 10, 19, 4, 52, 465775), {'2013': 167220, '2014': 166706, '2015': 166962, '2016': 166514, '2017': 166894, '2018': 165704}, 116900)

Finished in 4.4504356 seconds
```

### python good_perf.py
```
2020-03-10 19:03:55.985859, 2020-03-10 19:04:01.770386, {'2013': 167220, '2014': 166706, '2015': 166962, '2016': 166514, '2017': 166894, '2018': 165704}
'ao' was found 116899 times

Finished in 5.7992901 seconds
```
### dates was getting written to the wrong key
```
if new[0][6:] == '2018':
    year_count["2017"] += 1
```
### removed line[6] to prevent out of index error
```
if "ao" in line:
```

I initially wrote it to read the csv file into a dict with a header this seemed to have the most overhead coming from `(__next__)`

`python -m cProfile good_perf.py`
```
 1000002    3.123    0.000    5.729    0.000 csv.py:108(__next__)
```
I went back and rewrote it based on the original `poor_perf.py` as a plain `csv.reader` versus `csv.DictReader` this allowed me to eliminate calling `(__next__)` all together, 
filter easier, and iterate of the rows versus iterating over the keys in a dictionary each time. 

```
PS R:\uw_python\sp_online_py220b\students\billy_galloway\lesson_6\assignment> python good_perf.py
total time to finish 2.0548713, {'2013': 167288, '2014': 166804, '2015': 166856, '2016': 166695, '2017': 166780, '2018': 165577}
'ao' was found 116892 times

total time to finish 2.1895054, {'2013': 167288, '2014': 166804, '2015': 166856, '2016': 166695, '2017': 166780, '2018': 165577}
'ao' was found 116892 times
         1023165 function calls (1023080 primitive calls) in 2.228 seconds

   Ordered by: standard name
```
I Was able to get it down to 2 seconds this way and cutting the original time in half from `poor_perf.py`