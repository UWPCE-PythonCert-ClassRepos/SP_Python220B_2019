"""
Generate a million lines in data/exercise.csv.

~30% chance that 'ao' appears in a final column.
"""

import os
import csv
import random
import uuid
from datetime import date, timedelta

DIR = os.path.dirname(os.path.realpath(__file__))
FILE = os.path.join(DIR, 'data', 'exercise.csv')

START_DATE = date(2010, 1, 1)
END_DATE = date(2018, 12, 31)
DATE_DELTA = (END_DATE - START_DATE).days


def random_date():
    """Generate a random date."""

    return START_DATE + timedelta(days=random.randint(0, DATE_DELTA))


if __name__ == "__main__":

    guids = set()
    with open(FILE, newline='') as read_f:
        reader = csv.reader(read_f)
        for line in reader:
            guids.add(line[0])

    lines = len(guids)
    if lines < 1e6:  # Need to expand
        with open(FILE, 'a', newline='') as write_f:
            write_f.write('\n')
            writer = csv.writer(write_f)
            for i in range(lines, int(1e6)):
                guid = uuid.uuid1()
                while str(guid) in guids:  # Ensure it is a unique guid
                    guid = uuid.uuid1()
                guids.add(str(guid))

                # Write row
                writer.writerow([guid, i + 1, i + 2, i + 3, i + 4,
                                 random_date().strftime("%m/%d/%Y"),
                                 'ao' if random.randrange(0, 10) < 3 else ''])

        print(f"{FILE} expanded successfully")
    else:
        print("1 million entries already present")
