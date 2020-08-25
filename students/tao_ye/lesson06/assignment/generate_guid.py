"""
Python code to generate guid using uuid4()
"""

import uuid
import csv
from datetime import datetime, timedelta
import random

column_2, column_3, column_4, column_5 = 0, 1, 2, 3

with open('data/exercise.csv', 'w', newline='') as data_file:

    for i in range(1000000):
        new_id = uuid.uuid4()
        uuid_datetime = datetime(1000, 1, 1) + timedelta(microseconds=new_id.time // 10)
        column_6 = uuid_datetime.strftime('%m/%d/%Y')
        column_2 += 1
        column_3 += 1
        column_4 += 1
        column_5 += 1

        column_7 = random.choice(['ao', ''])
        data_row = [new_id, str(column_2), str(column_3), str(column_4), str(column_5),
                    column_6, column_7]

        data_writer = csv.writer(data_file)
        data_writer.writerow(data_row)
