import csv
import uuid
from datetime import date
import time
import random


def gen_random_id():
    limit = 1000
    for i in range(1, limit):
        random_id = uuid.uuid4()
    return random_id


def gen_random_date():
    """Generate random date between
    start_date and today date"""
    start_date = date(2008, 1, 1)
    end_date = date.today()
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%m/%d/%Y")


def write_to_csv(file_name):
    """Write to csv file"""
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for i in range(1, 1000000):
            content = []
            random_date = gen_random_date()
            random_id = str(gen_random_id())
            content.append(random_id)
            for i in range(0, 4):
                content.append(random.randint(1, 200))
            content.append(random_date)
            content.append(random.choice(['ao', None]))
            csv_writer.writerow(content)


if __name__ == '__main__':
    write_to_csv('data/exercise.csv')