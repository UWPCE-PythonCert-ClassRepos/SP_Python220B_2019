import csv
import uuid
from random import randint
import random
from datetime import datetime, timedelta


def generate_id():
	"""generate a random uuid"""
	random_id = uuid.uuid4()
	return str(random_id)


def generate_date(min_year=2013, max_year=2019):
	"""generate a random date"""
	start = datetime(min_year, 1, 1, 00, 00, 00)
	years = max_year - min_year + 1
	end = start + timedelta(days=365 * years)
	return (start + (end - start) * random.random()).strftime('%m/%d/%Y')


def expand_data(filename):
	"""expand data to 1mm rows"""
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file)
		for i in range(1, 1000000):
			csv_writer.writerow([generate_id(),
			                     randint(0, 100),
			                     randint(0, 100),
			                     randint(0, 100),
			                     randint(0, 20),
			                     generate_date(),
			                     random.choice(['ao', None])])


if __name__ == "__main__":
	expand_data('exercise.csv')
