# pylint: disable=invalid-name
"""Generate a CSV file with sample data"""
import csv
import uuid
from random import randrange
from datetime import datetime


def main():
    """Generate a CSV file with sample data"""
    with open('data/exercise.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(1000000):
            writer.writerow(build_row(i))


def build_row(i):
    """Build a row for the csv file"""
    # generate random guid
    guid = uuid.uuid4()

    # popoulate the 4 int columns
    num1 = i + 1
    num2 = i + 2
    num3 = i + 3
    num4 = i + 4

    # generate a random date between 1/1/2010 and 12/31/2019
    fdate = 1262304001
    ldate = 1577836799
    edate = randrange(fdate, ldate)
    date = datetime.fromtimestamp(edate).strftime("%m/%d/%Y")

    # add "ao" to 30% of rows
    ao = ""
    rand = randrange(1, 10)
    if rand <= 3:
        ao = "ao"

    # return formatted csv row
    return [guid, num1, num2, num3, num4, date, ao]


if __name__ == "__main__":
    main()
