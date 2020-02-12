"""
Functionality to generate additional test data.
"""

import csv
import random
import time
import uuid

def random_date(start_date='01/01/2010', end_date='12/31/2019'):
    """
    Generate a random date between start_date and end_date, and return in the same format.
    """
    start_time = time.mktime(time.strptime(start_date, '%m/%d/%Y'))
    end_time = time.mktime(time.strptime(end_date, '%m/%d/%Y'))
    random_time = start_time + random.random() * (end_time - start_time)
    return time.strftime('%m/%d/%Y', time.localtime(random_time))

def generate_data(filename, target_count):
    """
    Generate additional random data in filename.  target_count provides a declarative end-state
    for the count of records in the CSV.
    """
    with open(filename, 'r') as csvfile:
        # Evaluate whether the data file has a newline at the end of the file
        # Also get the current length so we know how many new lines to add
        dataset_asis = csvfile.readlines()
        current_count = len(dataset_asis)
        add_newline = not bool(dataset_asis[-1][-1] == '\n')

    with open(filename, 'a') as csvfile:
        if add_newline is True:
            # If there's no newline at the end, add one
            csvfile.write('\n')

        writer = csv.writer(csvfile, delimiter=',', quotechar='"')

        for i in range(current_count + 1, target_count + 1):
            # Add lines in the same format
            writer.writerow([uuid.uuid4(), i, i + 1, i + 2, i + 3, random_date(),
                             'ao' if random.random() > .5 else ''])

if __name__ == "__main__":
    generate_data('data/exercise.csv', 1000000)
