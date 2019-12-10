"""Expand input data from 10 records to 1,000,000 records"""

import uuid
import csv
from datetime import date
import random

def write_data(file_name):
    """Expand given input file to contain 1,000,000 rows of data"""
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])
        numbers = (10, 11, 12, 13)
        for _ in range(1000000):
            guid = uuid.uuid4()
            random_date = get_random_date(2000, 2019)
            random_ao = random.choice(['ao', None])
            numbers = tuple(map(increment, numbers))
            writer.writerow([guid, *numbers, random_date, random_ao])

def increment(num):
    """Return the incremented index by one"""
    return num + 1

def get_random_date(start_year, end_year):
    """Generate a random date between given years"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 1, 1)
    result = start_date + (end_date - start_date) * random.random()

    return result.strftime('%m/%d/%Y')

def main():
    """Main expand input function"""
    write_data('data/exercise.csv')

if __name__ == "__main__":
    # Call main function
    main()
