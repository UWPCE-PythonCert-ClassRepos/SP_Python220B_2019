""" 
    create 1,000,000 lines of randome data 
    usage: python create_random_data.py > exercise.csv
"""

import datetime
import random
import uuid

rows_of_data = 1000000
dt_start = datetime.date(2010, 1, 1)
dt_end = datetime.date(2018, 12, 31)
num_of_days = (dt_end - dt_start).days

### how to generate random dates
# ref: https://kite.com/python/answers/how-to-generate-a-random-date-between-two-dates-in-python

for x in range(rows_of_data):
    id = uuid.uuid4()
    num_list = [str(x+1), str(x+2), str(x+3), str(x+4)]
    random_date = (dt_start + datetime.timedelta(days=random.randrange(num_of_days))).strftime('%m/%d/%Y')
    ao_choice = random.choice(['', 'ao'])
    print('{},{},{},{}'.format(id, ','.join(num_list), random_date, ao_choice))
