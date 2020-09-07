"""create source file for lesson6 performance"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
# pylint: disable=W0612 # too many variables

import datetime
import random
import uuid
from csv import writer
import pandas as pd


class BuildCsvFile:
    """build csv file
    csv_file, full filename including path
    rows_to_add, count of rows to add to the file
    """

    def __init__(self, rows_to_add, csv_file):
        self.csv_file = csv_file
        self.rows_to_add = rows_to_add

    @staticmethod
    def random_date():
        """generate a random date"""
        start_date = datetime.date(2010, 1, 1)
        end_date = datetime.date(2018, 2, 1)
        gap = end_date - start_date
        days_between_dates = gap.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        formatted_date = (random_date.strftime('%m/%d/%Y'))
        return formatted_date

    @staticmethod
    def random_ao():
        """generates a random number"""
        random_num = 0
        result = ''
        for rand in range(10):
            random_num = random.randint(1, 10)
        if random_num < 5:
            result = 'ao'
        return result

    def add_rows(self):
        """add rows to the csv file"""

        row_cnt = self.rows_to_add
        csv_file = self.csv_file
        pandas_df = pd.read_csv(csv_file)
        df2 = pandas_df.iloc[[-1]]
        for index, row in df2.iterrows():
            c_two = row[1]
            c_three = row[2]
            c_four = row[3]
            c_five = row[4]
        for index in range(row_cnt):
            guid = uuid.uuid1()
            ran_date = BuildCsvFile.random_date()
            ran_ao = BuildCsvFile.random_ao()
            c_two += 1
            c_three += 1
            c_four += 1
            c_five += 1
            row_contents = [guid, c_two, c_three, c_four, c_five, ran_date, ran_ao]
            with open(csv_file, 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow(row_contents)
