"""
Append the provided csv data file to 1,000,000 records.
"""

import csv
import os
import uuid
import random
from datetime import date, timedelta


def append_csv_data(filename, num_of_rows=1000000):
    """
    :parm filename: existing csv data file.
    :parm num_of_rows: total number of rows generated
    """
    start_date = date(2012, 1, 1)
    end_date = date.today()
    max_days = (end_date - start_date).days
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        rows = [row for row in reader]
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        for row in rows:
            writer.writerow(row)
        for i in range(len(rows)+1, num_of_rows):
            uu_id = str(uuid.uuid4())
            a_o = random.choice(['ao', None])
            year = start_date + timedelta(days=random.randrange(0, max_days))
            writer.writerow([uu_id, i+1, i+2, i+3, i+4,
                             year.strftime('%m/%d/%Y'), a_o])


if __name__ == "__main__":
    FILE_NAME = os.path.join('data', 'exercise.csv')
    append_csv_data(FILE_NAME)
