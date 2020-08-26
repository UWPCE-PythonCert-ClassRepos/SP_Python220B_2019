import csv
import datetime
import random
import uuid

with open('exercise_data.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',')

    for i in range(1000000):
        if (i%100000 == 0):
            print(i)
        guid = str(uuid.uuid4())

        start_date = datetime.date(2010, 1, 1)
        end_date = datetime.date(2020, 12, 31)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        place_ao = random.randint(0, 4)

        ao = ''

        if (place_ao == 1):
            ao = 'ao'

        data_writer.writerow([guid, random.randint(0,1000), random.randint(0,1000), random.randint(0,1000), random.randint(0,1000), random_date.strftime("%m/%d/%Y"), ao])

