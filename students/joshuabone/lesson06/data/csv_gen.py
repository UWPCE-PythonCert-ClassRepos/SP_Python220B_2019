"""Generates random data in prescribed format and saves to CSV."""
import csv
import datetime
import random
import uuid

N_ROWS = 1_000_000


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.

    NOTE: I COPIED THIS FUNCTION FROM:
    https://stackoverflow.com/questions/553303/
    generate-a-random-date-between-two-other-dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def gen_row():
    """Randomly generate a single row in prescribed format."""
    row = list()
    # First entry is a UUID
    row.append(str(uuid.uuid4()))
    # Next 4 entries are random integers on interval [1, 100].
    for _ in range(4):
        row.append(random.randint(1, 101))
    rdate = random_date(datetime.date(2010, 1, 1),
                        datetime.date(2020, 1, 1))
    # Next entry is a random date on interval [01/01/2010, 12/31/2020]
    row.append(rdate.strftime("%m/%d/%Y"))
    # Next entry contains string 'ao' with 30% probability, else ''.
    if random.randint(1, 11) <= 3:
        row.append('ao')
    else:
        row.append('')
    return row


if __name__ == '__main__':
    with open('lesson06.csv', 'w') as csv_file:
        WRITER = csv.writer(csv_file)
        for _ in range(N_ROWS):
            WRITER.writerow(gen_row())
