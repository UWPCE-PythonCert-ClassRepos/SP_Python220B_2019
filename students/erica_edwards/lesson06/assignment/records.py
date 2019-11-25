""" Creates data for .csv file """

import uuid
from datetime import datetime, timedelta
import random

def random_date(min_year=2010):
    """Generate random date"""
   # generate a date in mm/dd/yyyy using datetime.
    start = datetime(min_year, 1, 1)
    day_range = 10 * 365
    result = start + timedelta(days=day_range * random.random())
    # print(result.strftime("%m/%d/%Y"))
    return result

def generate_data():
    """generate data for .csv file"""
    with open('records.csv', 'w') as csvfile:
        choices = ['ao', '', '']
        for i in range(0, 1000000):
            row = (f"{str(uuid.uuid4())},{i+1},{i+2},{i+3},{i+4}"
                   f",{random_date():%m/%d/%Y},{random.choice(choices)}\n")
            csvfile.write(row)



if __name__ == "__main__":
    # random_date()
    generate_data()
