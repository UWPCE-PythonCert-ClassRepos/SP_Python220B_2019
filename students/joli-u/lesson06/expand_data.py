
"""
expand_data.py
Assignment 6
Joli Umetsu
PY220
"""

from datetime import date, timedelta
from uuid import uuid4
import random
from csv import writer


def get_random_data():
    """
    Generates random ID and corresponding date for record data
    Returns: ID (string), date (string)
    """
    start = date(2010, 1, 1)
    end = date(2020, 1, 1)
    n = (end - start).days
    random_n_days = random.randrange(n)
    random_date = start + timedelta(days=random_n_days)
    random_id = uuid4()

    return random_id, random_date.strftime('%m/%d/%Y')


def main():
    with open('data/exercise.csv', 'a', newline='') as f:
        f_writer = writer(f)
        f_writer.writerow('\n')

        for row in range(11, 1000001):
            row_id, row_date = get_random_data()
            f_writer.writerow([row_id, row, row+1, row+2, row+3, row_date, random.choice(('ao', None, None))])

if __name__ == "__main__":
    main()