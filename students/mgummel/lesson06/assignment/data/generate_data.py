"""generate data module"""
import uuid
import csv
import random
from datetime import date
from datetime import timedelta


def generate_ao():
    """
    Generates a value for the last column randomly.
    All values will either be an empty string or the
    string 'ao'
    :return: '' or "ao"
    """
    ao_value = ''

    rand_value = random.randint(1, 2)
    if rand_value == 2:
        ao_value = "ao"
    return ao_value


def generate_random_date():
    """
    Generate a random date and format it to a string
    to use for the date column in a csv file
    :return: formatted date string
    """
    start_date = date(2010, 1, 1)
    end_date = date(2019, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    formatted_date = random_date.strftime("%m/%d/%Y")

    return formatted_date


def main():
    """
    Opens a file called exercise.csv and appends generated
    data to it. Will call all methods in the generate_data
    module.
    :return: n/a
    """

    with open('exercise.csv', 'a', newline='') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow('\n')

        for i in range(1, 1000001):
            generated_data = list()
            generated_data.append(str(uuid.uuid4()))

            for number in range(i, i + 4):
                generated_data.append(number)

            generated_data.append(generate_random_date())
            generated_data.append(generate_ao())

            csv_write.writerow(generated_data)


if __name__ == '__main__':
    main()
