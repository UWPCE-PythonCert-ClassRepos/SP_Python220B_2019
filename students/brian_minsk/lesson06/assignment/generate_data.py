""" Script to generate a data file for the lesson06 assignment.
"""

from datetime import date, timedelta
import locale
from random import randrange, choice
from uuid import uuid4
import csv

def random_date_between(start=(2010, 1, 1), end=(2019, 12, 31)):
    """ Generate a random date between two dates.

    Keyword arguments:
    start - the lower date represented by a tuple of the form (year, month, day)
    end - the upper date represented by a tuple of the form (year, month, day)
    """
    date_lower = date(start[0], start[1], start[2])
    date_higher = date(end[0], end[1], end[2])

    delta = date_higher - date_lower

    rand_days = randrange(delta.days)
    return date_lower + timedelta(rand_days)


def write_data(file_name="lesson06_data.csv", lines=1000000):
    """ Write a csv file of the format below, with a uuid in the first column, a US formatted date
    int the sixth column, and randomly inserted "ao" in column seven (probability of 1/3 that "ao"
    is inserted).

    5df44a54-8cca-4928-bc53-caabb23cf329,1,2,3,4,05/26/2015,
    bc337622-119c-445d-9282-e4b980201c03,2,3,4,5,08/02/2011,ao
    f7a66f58-cfb2-459b-aca7-7eebd6f5417d,3,4,5,6,04/26/2017,
    5536f39e-9bdc-4bd6-8adb-1de901b5d68a,4,5,6,7,10/19/2010,
    23e918c3-19c4-4e78-9f1d-65041e22e6e8,5,6,7,8,01/27/2018,
    8f9ca0ad-cfce-4394-9114-17c6cf71965e,6,7,8,9,03/14/2018,
    d220e0d0-78f3-4ce4-b288-20b90bb6f328,7,8,9,10,03/30/2017,ao
    04f3967b-c7ba-4e8e-8026-aaffb8d5f0cc,8,9,10,11,12/19/2010,ao
    fbf0cf0d-886b-40c5-9259-bf38185ce95f,9,10,11,12,01/24/2011,
    c1cecf3f-9ad5-4546-87bf-cfb2bc4fa519,10,11,12,13,07/23/2010,

    Keyword arguments:
    file_name - filename
    lines - number of lines in the csv file
    """
    locale.setlocale(locale.LC_ALL, "en_US.utf8")  # use US date formatting

    with open(file_name, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        for i in range(1, lines + 1):
            ao_string = ""
            if choice((False, False, True)):
                ao_string = "ao"

            data_writer.writerow([str(uuid4()),
                                  i, i + 1, i + 2, i + 3,
                                  random_date_between().strftime("%m-%d-%Y"),
                                  ao_string])


if __name__ == "__main__":
    write_data()
