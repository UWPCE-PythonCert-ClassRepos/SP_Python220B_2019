"""
Make Random Data for Assignment
"""
import csv
from datetime import datetime
from random import randint, uniform
import uuid

def ao():
    """Randomly fill cell with ao"""

    if randint(0, 1) > 0:
        return 'ao'
    else:
        return ''

def gen_date():
    """Generate random data"""

    start_date = datetime(2011, 1, 1)
    end_date = datetime(2020, 5, 1)
    random_date = start_date + (end_date-start_date) * uniform(0, 1)

    return random_date.strftime("%m/%d/%Y")

def gen_hw_data():
    """Write csv with random data"""

    old_file = 'exercise.csv'

    with open(old_file, 'w', newline="\n") as new_file:
        csv_writer = csv.writer(new_file)

        for i in range(1,1000001):
            csv_writer.writerow([str(uuid.uuid1()), randint(0,11),
                                 randint(0,11), randint(0,20),
                                 randint(0,20), gen_date(), ao()])
if __name__ == "__main__":
    """Create new data for homework"""
    gen_hw_data()
