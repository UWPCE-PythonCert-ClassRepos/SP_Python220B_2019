"""Module for generating random customer, product, and rental data .csvs for testing."""

from csv import writer
from random import randrange, choice, randint, sample, random
import string
from datetime import datetime
# from random_word import RandomWords -- Module not working, gives error that no results found


def write_random_customers(filename, start_row, end_row):
    """Write random customers to filename.csv, between start row and end row"""
    customers = ((
        row,
        ' '.join((make_random_word(3, 8).title(),
                  make_random_word(3, 10).title())),
        ' '.join((str(randrange(1, 10000)),
                  make_random_word(4, 10).title(),
                  choice(('St', 'Rd', 'Ave')))),
        '{:03d}-{:03d}-{:04d}'.format(randrange(100, 999), randrange(0, 999), randrange(0, 9999)),
        make_random_word(2, 12) +
        choice(('@gmail.com', '@yahoo.com', '@hotmail.com')))
                 for row in range(start_row, end_row + 1))

    with open(filename, 'a', newline='') as file:
        csw_writer = writer(file)
        csw_writer.writerows(customers)


def write_random_products(filename, start_row, end_row):
    """Write random product data to filename.csv, between start row and end row"""
    num_rows = (end_row - start_row + 1)
    product_ids = sample(range(1, num_rows * 10), num_rows)
    products = ((
        product_id,
        ' '.join((make_random_word(3, 10).title(), make_random_word(3, 10).title())),
        choice(('Electric Appliance', 'General Decor', 'Home Furniture', 'Business Furniture')),
        randint(0, 99))
                for row, product_id in zip(range(start_row, end_row + 1), product_ids))

    with open(filename, 'a', newline='') as file:
        csw_writer = writer(file)
        csw_writer.writerows(products)

    return product_ids


def write_random_rentals(rentals_filename, product_ids, start_row, end_row):
    """Write random rental data to filename.csv, between start row and end row"""
    start_date = datetime(2010, 1, 1)
    end_date = datetime.today()
    rental_start_dates = (rand_date(start_date, end_date) for _ in range(start_row, end_row + 1))
    products = ((
        row,
        choice(product_ids),
        randint(1, 1000),
        rental_start_date,
        choice(('None', rand_date(datetime.strptime(rental_start_date, '%m/%d/%Y'), end_date))))
                for row, rental_start_date in zip(range(start_row, end_row + 1),
                                                  rental_start_dates))

    with open(rentals_filename, 'a', newline='') as file:
        csw_writer = writer(file)
        csw_writer.writerows(products)


def make_random_word(min_length, max_length):
    """Makes a random grouping of letters"""
    length = randint(min_length, max_length)
    return ''.join(choice(string.ascii_lowercase) for _ in range(length))


def rand_date(start_date, end_date):
    """Returns a random date between start_date and end_date."""
    new_date = start_date + (end_date - start_date) * random()
    return datetime.strftime(new_date, '%m/%d/%Y')


def main():
    """Main module run function."""
    write_random_customers('customers.csv', 1, 10000)
    product_ids = write_random_products('products.csv', 1, 10000)
    write_random_rentals('rentals.csv', product_ids, 1, 10000)


if __name__ == '__main__':
    main()
