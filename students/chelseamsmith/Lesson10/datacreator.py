"""adds entries to a specified csv file"""
import csv
import random
from datetime import date

def random_date():
    """generates a random date"""
    start = date(2010, 1, 1)
    end = date.today()

    chosen = start + (end - start) * random.random()

    return chosen.strftime("%m/%d/%Y")


def generate_data_cust():
    """generates customer data"""
    with open('csvfiles/customers_long.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, 50000):
            entry = ["user{}".format(i+1)]
            entry.append("name{}".format(i+1))
            entry.append("address{}".format(i+1))
            entry.append("phone{}".format(i+1))
            entry.append("email{}".format(i+1))
            csvwriter.writerow(entry)


def generate_data_prod():
    """generates product data"""
    with open('csvfiles/products_long.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, 50000):
            entry = ["prd{}".format(i+1)]
            entry.append("description{}".format(i+1))
            entry.append("category{}".format(i+1))
            entry.append(random.randrange(0, 10))
            csvwriter.writerow(entry)


def generate_data_rentals():
    """generates rental data"""
    with open('csvfiles/rentals_long.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, 50000):
            date_one = random_date()
            date_two = random_date()
            if date_one < date_two:
                start_date = date_one
                end_date = date_two
            else:
                start_date = date_two
                end_date = date_one
            entry = ["prd{}".format(i+1)]
            entry.append("user{}".format(i+1))
            entry.append("category{}".format(i+1))
            entry.append(start_date)
            entry.append(end_date)
            entry.append(random.randrange(2, 9))
            csvwriter.writerow(entry)


if __name__ == '__main__':
    generate_data_cust()
    generate_data_prod()
    generate_data_rentals()
