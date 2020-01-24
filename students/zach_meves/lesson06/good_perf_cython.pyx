"""
Cython version of good_perf.py
"""

import datetime
import csv
import Cython

def analyze(str filename):
    return canalyze(filename)

cdef canalyze(str filename):
    start = datetime.datetime.now()

    cdef int found
    found = 0

    csvfile = open(filename)
    #with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    cdef dict year_count
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    for row in reader:
        year = row[5][-4:]
        if year in year_count:
            year_count[year] += 1

        if 'ao' in row[6]:
            found += 1

    csvfile.close()

    # Re-create the 'bug' found in poor_perf.py
    year_count['2017'] += year_count['2018']
    year_count['2018'] = 0

    print(year_count)

    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return start, end, year_count, found
