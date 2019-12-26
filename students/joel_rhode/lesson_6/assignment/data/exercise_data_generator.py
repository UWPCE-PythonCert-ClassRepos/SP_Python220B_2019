"""Module containing function to generate large number of exercise data and write to csv."""
from uuid import uuid4
from datetime import datetime
from csv import writer
from random import choice, random


def generate_exercise_data(filename, start_line, end_line, start_date, end_date):
    """Generates exercise data, writing to csv from start line to end line."""
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    with open(filename, 'a', newline='') as file:
        writer(file).writerows((uuid4(), row, row + 1, row + 2, row + 3,
                                rand_date(start_date, end_date), choice((None, None, 'ao')))
                               for row in range(start_line, end_line + 1))


def rand_date(start_date, end_date):
    """Returns a random date between start_date and end_date."""
    new_date = start_date + (end_date - start_date) * random()
    return datetime.strftime(new_date, '%m/%d/%Y')


if __name__ == '__main__':
    generate_exercise_data('exercise.csv', 11, 1000000, '1/1/2010', '12/31/2019')
