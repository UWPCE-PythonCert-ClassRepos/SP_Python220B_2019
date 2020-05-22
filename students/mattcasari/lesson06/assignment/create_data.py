""" Lesson 06 Data Generator """

#pylint: disable=expression-not-assigned

from datetime import datetime as dt
from uuid import uuid4
from random import randrange, choice

DATETIME_MIN = dt.timestamp(dt(2010, 1, 1))
DATETIME_MAX = dt.timestamp(dt(2020, 12, 31))


def create_random_data():
    """
    Create Random Data String

    Generator that creates a string of data in the form:
    GUID, idx, idx+1, idx+2, idx+3, MM/DD/YYYY, [ao or nothing]
    """
    idx = 1
    while True:
        r_date = dt.fromtimestamp(randrange(DATETIME_MIN, DATETIME_MAX)).strftime(
            "%m/%d/%Y"
        )
        data = f"{str(uuid4())},{idx},{idx+1},{idx+2},{idx+3},{r_date},{choice(['ao',''])}\n"
        yield data
        idx += 1


def main():
    """
    Main run function.

    Generates 1 million data lines in a csv titled "exercise.csv"
    """
    data_gen = create_random_data()
    with open("exercise.csv", "w+") as csv_file:
        [csv_file.write(next(data_gen)) for x in range(1000000)]


if __name__ == "__main__":
    main()
