""" Add to data file, make rand data"""

import csv
import uuid
from datetime import date
import random

start_date = date(2011, 1, 1).toordinal()
end_date = date(2020, 5, 1).toordinal()
data_file = 'exercise.csv'
with open(r'data_file', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    for i in range(1, 1000001):
        writer.writerow([uuid.uuid1(), i, i + 1, i + 2, i + 3,
                         date.fromordinal(random.randint(start_date, end_date)),
                         random.choice(['ao'])])


                                    