import csv
import uuid
import random
from datetime import date

with open('./data\\exercise.csv', 'w', newline='') as csvfile:
    for i in range(0, 1000000, 1):
        mywriter = csv.writer(csvfile, delimiter=',')
        unique_id = str(uuid.uuid4())

        start = date(2010, 1, 1).toordinal()
        end = date.today().toordinal()
        random_date = date.fromordinal(random.randint(start, end)).strftime('%m/%d/%Y')

        ao = ""
        myint = random.randint(1,10)
        if myint > 7: ao = "ao"

        mywriter.writerow([unique_id, i, i+1, i+2, i+3, random_date, ao])
