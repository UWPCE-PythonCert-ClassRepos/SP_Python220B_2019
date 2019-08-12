"""
program to generate one million records
"""
import logging
import csv
from uuid import uuid4
import random
from datetime import timedelta, date

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def read_csv(filename):
    """
    Read existing CSV file.
    :param filename: Input path of the csv file.
    :return: Rows in existing csv file.
    """
    logging.info('Reading csv file...')
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        rows = list(row for row in reader)
        return rows


def generate(existing, number_of_rows=1000000):
    """
    Generate new rows.
    :param existing: Existing data to be extended.
    :param number_of_rows: Number of rows to be generated.
    :return: All rows to be written in csv file.
    """
    base_date = date(2008, 8, 8)
    days_limit = (date.today() - base_date).days
    result = existing
    logging.info('Generating new rows...')
    for i in range(len(existing), number_of_rows):
        guid = str(uuid4())
        r_date = base_date + timedelta(days=random.randrange(0, days_limit))
        ao = random.choice(['ao', ''])
        result.append(
            (guid, i + 1, i + 2, i + 3, i + 4, r_date.strftime('%m/%d/%Y'), ao)
        )
    logging.info('New rows generated...')
    return result


def write_csv(filename, data):
    """
    Write rows to csv file.
    :param filename: Output path for csv file.
    :param data: Data to be written.
    :return: None
    """
    logging.info('Writing to csv file...')
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerows(data)
    logging.info('CSV file generated...')


if __name__ == "__main__":
    existing_rows = read_csv('exercise.csv')
    generated = generate(existing_rows, 1000000)
    write_csv('exercise2.csv', generated)
