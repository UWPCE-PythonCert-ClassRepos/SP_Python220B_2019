"""Functions for generating fake CSV data."""
import csv
import random

N_CUSTOMERS = 100


def read_lines(filename):
    "Read lines and strip extra whitespace/newlines."
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


FIRST_NAMES = read_lines('first_names.txt')
LAST_NAMES = read_lines('last_names.txt')
CONCRETE_NOUNS = read_lines('concrete_nouns.txt')


def random_name():
    """Generates a random First Name + Last Name string."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def random_product_code():
    """
    Generates a random product code consisting of two uppercase letters
    followed by two digits.
    """
    num_part = random.randint(0, 100)
    letter_part = random.choice(LETTERS) + random.choice(LETTERS)
    return f"{letter_part}{num_part}"


def random_product():
    """Create a product with the given id and a random quantity."""
    product_code = random_product_code()
    description = random.choice(CONCRETE_NOUNS)
    price = f"{random.randint(1, 101):.2f}"
    return [product_code, description, price]


def write_csv(data, filename):
    """Write the data to csv with the given filename."""
    with open(filename, 'w') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(data)


if __name__ == "__main__":
    CUSTOMERS = []
    for i in range(N_CUSTOMERS):
        CUSTOMER = random_name()
        N_RECORDS = random.randint(1, 101)
        FNAME = "records_" + CUSTOMER.replace(" ", "_") + str(N_RECORDS) \
                + ".csv"
        RECORDS = [random_product() for _ in range(N_RECORDS)]
        write_csv(RECORDS, FNAME)
        CUSTOMERS.append((CUSTOMER, FNAME, N_RECORDS))
    with open('customer_records.csv', 'w') as customer_records_file:
        CSV_WRITER = csv.writer(customer_records_file)
        CSV_WRITER.writerows(CUSTOMERS)
