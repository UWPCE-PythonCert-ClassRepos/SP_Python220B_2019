"""
Adds to existing customer_file.csv, product_file.csv, and rental_file.csv per recommendations.
"""
import datetime
import random
import os
import sys
import csv

sys.path.append(os.getcwd())
src_dir = os.getcwd() + '/src_data/'


def generate_customers(number_entries):
    """
    Generate customer data as a list of lists.
    """
    customers = [['CID{:04d}'.format(i), 'last{}, first{}'.format(i, i),
                  'address{:04d}'.format(i), str(5553331111 + i), 'email{:04d}@xx.xx'.format(i)]
                  for i in range(1, number_entries)]

    return customers

def generate_products(number_entries):
    """
    Generate product data as a list of lists.
    """
    products = [['PID{:04d}'.format(i), 'P_Description{:04d}'.format(i),
                 random.choice(['Living Room', 'Bedroom', 'Kitchen', 'Dining Room', 'Office']),
                 str(random.randint(0, 40)), str(random.randint(1, 5))] for i in range(1, number_entries)]

    return products


def date_generator(s_or_f, cut_date=None):
    """
    Helper function for date generation
    """
    if s_or_f == 'start':
        beginning_date = datetime.date(2010, 1, 1)
        finish_date = datetime.date(2020, 4, 3)
    if s_or_f == 'finish':
        beginning_date = cut_date
        finish_date = datetime.date(2023, 4, 3)

    days_between_dates = (finish_date - beginning_date).days
    selected_date = beginning_date +\
                    datetime.timedelta(days=random.randrange(days_between_dates))
    generated_date = selected_date.strftime('%Y-%m-%d')

    return generated_date


def generate_rentals(customers, products, number_entries):
    """
    Generate rental data based on the customer and product data.
    """
    CIDs = [customer[0] for customer in customers]
    PIDs = [product[0] for product in products]
    start_dates = [date_generator('start') for i in range(1, number_entries)]
    end_dates = [date_generator('finish',
                 datetime.datetime.strptime(start_date, '%Y-%m-%d').date())
                 for start_date in start_dates]


    rentals = [[str(i), random.choice(CIDs), random.choice(PIDs),
                random.choice([random.randint(1, 4), random.randint(10, 25)]),
                start_date, end_date] for i, start_date, end_date in
                zip(range(1, number_entries), start_dates, end_dates)]

    return rentals


def write_data(customers, products, rentals, entry_response):
    """
    Write new data to the existing file.
    """

    file_paths = [src_dir + 'customer_file_{}.csv'.format(entry_response),
                  src_dir + 'product_file_{}.csv'.format(entry_response),
                  src_dir + 'rental_file_{}.csv'.format(entry_response)]

    headers = [['user_id,name', 'address', 'phone_number', 'email'], ['product_id', 'description',
               'product_type', 'quantity_available', 'daily_rate'], ['rental_id', 'user_id',
               'product_id', 'quantity_rented', 'start_date', 'end_date']]

    data_sets = [customers, products, rentals]

    for file_path, header, data_set in zip(file_paths, headers, data_sets):
        with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(data_set)


def main():
    entry_response = int(input("Please enter how many entries are desired (max 9999): "))
    number_entries = entry_response + 1
    customers = generate_customers(number_entries)
    products = generate_products(number_entries)
    rentals = generate_rentals(customers, products, number_entries)
    write_data(customers, products, rentals, entry_response)
    return entry_response


if __name__ == "__main__":
    main()
