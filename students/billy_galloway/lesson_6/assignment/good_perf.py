"""
poorly performing, poorly written module

"""
import csv
import generate_data
import time

def analyze(filename):
    ''' 
        ingests csv file and returns a tuple with
        a start time, end time, all the years found
        between 2013 and 2018
        and how many times that ao showed up in a row
    '''
    start = time.perf_counter()
    year_count = {
        '2013': 0,
        '2014': 0,
        '2015': 0,
        '2016': 0,
        '2017': 0,
        '2018': 0
    }

    found = 0

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lrow = list(row)
            date = f'{lrow[5]}'.split('/')
            year_count[date[-1]]+=1
            if 'ao' in row:
                found+=1

    end = time.perf_counter()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise-00.csv"
    # generate_data.write_csv(filename)
    output = analyze(filename)
    total_time = output[1]-output[0]
    print(f"total time to finish {total_time}, {output[2]}\n\'ao\' was found {output[3]} times")

if __name__ == "__main__":
    main()
