"""
poorly performing, poorly written module

"""
from datetime import datetime
from timeit import timeit as timer
import csv
import generate_data

def is_year(input_list):
    ''' searches for dates in dictionary '''
    date = input_list['date'].split('/')
    return date[-1]

def total_years(years_list):
    ''' takes a list of years and returns a dictionary '''
    year_count = {
        '2013': 0,
        '2014': 0,
        '2015': 0,
        '2016': 0,
        '2017': 0,
        '2018': 0
    }

    for year in years_list:
        year_count[year]+=1

    return year_count

def analyze(filename):
    ''' ingests csv file and returns a list of dictionaries '''
    start = datetime.now()
    output_list = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for line in reader:
            output_list.append({
                'guid': line['guid'],
                'entry': line['count_0'],
                'date': line['date'],
                'ao': line['ao']
            })

        return output_list, start

def return_output(analyze_output):
    # return a list of years
    years = list(map(is_year, filter(lambda x: x['date'], analyze_output)))
    year_count = total_years(years)

    # returns the total times ao is found
    found = len(list(filter(lambda x: x['ao'], analyze_output)))
    end = datetime.now()
    return (end, year_count, found)

def main():
    filename = "data/exercise-00.csv"
    csv_output, start = analyze(filename)
    returned_output = return_output(csv_output)
    print(f"{start}, {returned_output[0]}, {returned_output[1]}\n\'ao\' was found {returned_output[2]} times")

if __name__ == "__main__":
    main()
