"""
Adds to existing customer_file.csv, product_file.csv, and rental_file.csv per recommendations.
"""
import datetime
import random
import csv


def generate_customers():
    """
    Generate customer data as a list of lists.
    """
    customers = [['CID{:04d}'.format(i), 'last{}, first{}'.format(i, i),
                  'address{:04d}'.format(i), str(5553331111 + i), 'email{:04d}@xx.xx'.format(i)]
                  for i in range(6, 10000)]

    return customers

def generate_products():
    """
    Generate product data as a list of lists.
    """
    products = [['PID{:04d}'.format(i), 'P_Description{:04d}'.format(i),
                 random.choice(['Living Room', 'Bedroom', 'Kitchen', 'Dining Room', 'Office']),
                 str(random.randint(0, 40)), str(random.randint(1, 5))] for i in range(9, 10000)]

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


def generate_rentals(customers, products):
    """
    Generate rental data based on the customer and product data.
    """
    CIDs = [customer[0] for customer in customers]
    PIDs = [product[0] for product in products]
    start_dates = [date_generator('start') for i in range(16, 10000)]
    end_dates = [date_generator('finish',
                 datetime.datetime.strptime(start_date, '%Y-%m-%d').date())
                 for start_date in start_dates]


    rentals = [[str(i), random.choice(CIDs), random.choice(PIDs),
                random.choice([random.randint(1, 4), random.randint(10, 25)]),
                start_date, end_date] for i, start_date, end_date in
                zip(range(16, 10000), start_dates, end_dates)]

    return rentals


def write_data(customers, products, rentals):
    """
    Write new data to the existing file.
    """
    source_path = ('/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/' +
                 'cjfortu/L07/assignment/src_data/')

    file_paths = [source_path + 'customer_file.csv',
                  source_path + 'product_file.csv',
                  source_path + 'rental_file.csv']

    data_sets = [customers, products, rentals]

    for file_path, data_set in zip(file_paths, data_sets):
        with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([])
            csv_writer.writerows(data_set)



# def generate_date_info():
#     """
#     Return data required for random date generation.
#     """
#     start_date = datetime.date(2010, 1, 1)
#     end_date = datetime.date(2018, 12, 31)
#     days_between_dates = (end_date - start_date).days

#     return days_between_dates, start_date


# def write_data(days_between_dates, start_date):
#     """
#     Write new data to the existing file.
#     """
#     file_path = ('/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/' +
#                  'cjfortu/L06/assignment/data/exercise.csv')

#     all_data = [[uuid.uuid4(), 10 + i, 11 + i, 12 + i, 13 + i,
#                  (start_date + datetime.timedelta(days=random.randrange(days_between_dates))).
#                  strftime('%m/%d/%Y'),
#                  random.choice(['ao', ''])] for i in range(1, 999991)]

#     with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow([])
#         csv_writer.writerows(all_data)


if __name__ == "__main__":
    CUSTOMERS = generate_customers()
    PRODUCTS = generate_products()
    RENTALS = generate_rentals(CUSTOMERS, PRODUCTS)
    write_data(CUSTOMERS, PRODUCTS, RENTALS)
