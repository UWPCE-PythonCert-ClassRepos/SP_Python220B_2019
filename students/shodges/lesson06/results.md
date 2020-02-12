## Analysis Overview
| Timing Method  | Baseline | [Change 1](#good_perf-change-1) | [Change 2](#good_perf-change-2) |
| -------------- | -------- | ------------------------------- | ------------------------------- |
| Timestamp diff | 4.204673 | 2.432901                        | 2.123108                        |
| time -p        | 4.12     | 2.70                            | 2.16                            |
## Initial analysis of poor_perf.py
These tests establish the baseline utilizing the following analyze() function:
```python
def analyze(filename):
    """
    Analyze filename for data trends.
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)
```
With 1,000,000 records, analyze() took 4.204673 seconds according to the difference in timestamps:
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
And 4.12 seconds according to time:
```
shodges-ltm:lesson06 shodges$ time -p python3 poor_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 4.12
user 4.00
sys 0.10
```

## good_perf change 1
I removed the for loop that processed the CSV a second time and moved its analysis into the primary for loop:
```python
def analyze(filename):
    """
    Analyze filename for data trends.
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        for row in reader:
            lrow = list(row)
            if "ao" in row[6]:
                found += 1
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)
```
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

## good_perf change 2
I removed the usage of new_ones (and the secondary processing for loop) and moved the date analysis to the primary for loop:
```python
def analyze(filename):
    """
    Analyze filename for data trends.
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            lrow = list(row)
            if "ao" in row[6]:
                found += 1

            if row[5][6:] == '2013':
                year_count["2013"] += 1
            if row[5][6:] == '2014':
                year_count["2014"] += 1
            if row[5][6:] == '2015':
                year_count["2015"] += 1
            if row[5][6:] == '2016':
                year_count["2016"] += 1
            if row[5][6:] == '2017':
                year_count["2017"] += 1
            if row[5][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)
```
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
