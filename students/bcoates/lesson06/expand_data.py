""" Expand original CSV with more dummy data """

import csv
import uuid
import random
from datetime import date, timedelta

DATA_FILE = "data/exercise.csv"

def get_last_line(input_file):
    """ Reads the last line and returns a list """

    with open(input_file) as csv_file:
        all_lines = csv_file.readlines()
        last_line = all_lines[-1].split(",")
        return last_line

def add_one(x_value):
    """ Add 1 to an integer """

    return x_value + 1

def random_date():
    """ Generate a random date """

    start_date = date(2010, 1, 1)
    end_date = date.today()
    day_range = (end_date - start_date).days
    new_random_date = start_date + timedelta(days=random.randint(1, day_range))
    return new_random_date.strftime('%m/%d/%Y')

def main():
    """ Main function to expand data """

    starting_list = get_last_line(DATA_FILE)

    col_b = int(starting_list[1])
    col_c = int(starting_list[2])
    col_d = int(starting_list[3])
    col_e = int(starting_list[4])

    with open(DATA_FILE, "a") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerow([])

        for _ in range(1000000):
            col_a = uuid.uuid4()
            col_b, col_c, col_d, col_e = map(add_one, [col_b, col_c, col_d, col_e])
            col_f = random_date()
            col_g = random.choice(["ao", None])
            writer.writerow([col_a, col_b, col_c, col_d, col_e, col_f, col_g])

if __name__ == "__main__":
    main()
