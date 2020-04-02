"""
Adds to existing exercise.csv file per requirements.
"""
import datetime
import random
import uuid
import csv


def generate_date_info():
    """
    Return data required for random date generation.
    """
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2018, 12, 31)
    days_between_dates = (end_date - start_date).days

    return days_between_dates, start_date


def write_data(days_between_dates, start_date):
    """
    Write new data to the existing file.
    """
    file_path = ('/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/' +
                 'cjfortu/L06/assignment/data/exercise.csv')

    all_data = [[uuid.uuid4(), 10 + i, 11 + i, 12 + i, 13 + i,
                 (start_date + datetime.timedelta(days=random.randrange(days_between_dates))).
                 strftime('%m/%d/%Y'),
                 random.choice(['ao', ''])] for i in range(1, 999991)]

    with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([])
        csv_writer.writerows(all_data)


if __name__ == "__main__":
    DAYS_BETWEEN_DATES, START_DATE = generate_date_info()
    write_data(DAYS_BETWEEN_DATES, START_DATE)
