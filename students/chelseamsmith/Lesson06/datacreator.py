"""adds entries to a specified csv file"""
import csv
import uuid
import random
from datetime import date

def random_date():
    """generates a random date"""
    start = date(2010, 1, 1)
    end = date.today()

    chosen = start + (end - start) * random.random()

    return chosen.strftime("%m/%d/%Y")



def generate_data():
    """generates data in a csv file"""
    with open('data/exercise.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, 1000000):
            entry = [str(uuid.uuid4())]
            entry.append(i + 1)
            entry.append(i + 2)
            entry.append(i + 3)
            entry.append(i + 4)
            entry.append(random_date())
            entry.append(random.choice(['ao', None]))
            csvwriter.writerow(entry)

if __name__ == '__main__':
    generate_data()
