"""
Good performing module

"""
import csv
import datetime
from statistics import mean
from timeit import repeat

def analyze(filename):
    
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

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
            if row[5][6:] in year_count.keys():
                year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    
    reps = 10
    test = '''filename = "data/exercise.csv"
analyze(filename)'''

    timer = repeat(stmt=test, globals=globals(),
                  repeat=reps,number=1)

    print('The average of ' + str(reps) + ' runs of the good_perf module timeit runs:')
    print(mean(timer))


if __name__ == "__main__":
    main()
