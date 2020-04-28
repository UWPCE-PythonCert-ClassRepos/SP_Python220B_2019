import uuid
import csv
import random


def data_adder(file):
    with open(f'./data/{file}.csv', "a", newline="") as f:
        i = 1
        while i<=1000000:
            random_day = random.randint(1,28)
            random_month = random.randint(1,12)
            random_year = random.randint(2000,2020)
            random_int = random.randint(0,1)
            writer = csv.writer(f, delimiter=",")
            if random_int == 0:
                writer.writerow([uuid.uuid4(), i, i+1, i+2, i+3, f"{random_month}/{random_day}/{random_year}", ""])
            elif random_int == 1:
                writer.writerow([uuid.uuid4(), i, i+1, i+2, i+3, f"{random_month}/{random_day}/{random_year}", "ao"])
            i += 1


if __name__ == '__main__':
    data_adder("exercise")
