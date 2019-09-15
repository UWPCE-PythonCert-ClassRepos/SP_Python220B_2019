from random import randint, uniform
import uuid
from datetime import datetime
import csv

def make_date():
    """Makes random dates between 2010 and 2019"""
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2020, 1, 1)
    random_date = start_date + (end_date-start_date)*uniform(0, 1)
    return random_date.strftime("%m/%d/%Y")

def yes_ao():
    if randint(0,1)>0:
        return "ao"
    else:
        return ""

def make_file():
    file = 'exercise.csv'

    with open(file, 'w', newline="\n") as my_file:
        person_writer = csv.writer(my_file)

        for i in range(1,1000000):
            person_writer.writerow([str(uuid.uuid4()), randint(0,20), randint(0,20), randint(0,20),
                                    randint(0,20), make_date(), yes_ao()])


if __name__ == '__main__':
    make_file()