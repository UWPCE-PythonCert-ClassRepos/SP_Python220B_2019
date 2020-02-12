## Analysis Overview
| Timing Method  | Baseline | [Change 1](#good_perf-change-1) | [Change 2](#good_perf-change-2) |
| -------------- | -------- | ------------------------------- | ------------------------------- |
| Timestamp diff | 4.204673 | 2.522429                        | 2.26                            |
| time -p        | 4.12     | 2.61                            | 2.293705                        |
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
With this change, the timestamp diff shows 2.522429 seconds and time shows a runtime of 2.61 seconds.
```
>>> import good_perf
>>> good_results_1 = good_perf.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
>>> good_results_1
(datetime.datetime(2020, 2, 12, 14, 5, 18, 766950), datetime.datetime(2020, 2, 12, 14, 5, 21, 289379), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}, 500161)
>>> good_results_1[1] - good_results_1[0]
datetime.timedelta(seconds=2, microseconds=522429)
```
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 2.61
user 2.52
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
Timestamp diffs now show a runtime of 2.293705 seconds and time shows a runtime of 2.26 seconds.
```
shodges-ltm:lesson06 shodges$ time -p python3 good_perf.py
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
real 2.26
user 2.22
sys 0.02
```
```
>>> import good_perf
>>> good_results_2 = good_perf.analyze('data/exercise.csv')
{'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}
'ao' was found 500161 times
>>> good_results_2
(datetime.datetime(2020, 2, 12, 14, 28, 30, 813596), datetime.datetime(2020, 2, 12, 14, 28, 33, 107301), {'2013': 100148, '2014': 99915, '2015': 100652, '2016': 100129, '2017': 199631, '2018': 0}, 500161)
>>> good_results_2[1] - good_results_2[0]
datetime.timedelta(seconds=2, microseconds=293705)
```
