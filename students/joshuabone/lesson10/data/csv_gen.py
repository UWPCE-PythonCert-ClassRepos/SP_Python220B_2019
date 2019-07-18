"""Functions for generating fake CSV data."""
import csv
import random


def read_lines(filename):
    "Read lines and strip extra whitespace/newlines."
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


FIRST_NAMES = read_lines('first_names.txt')
LAST_NAMES = read_lines('last_names.txt')
CITY_STATES = read_lines('city_state.txt')
CONCRETE_NOUNS = read_lines('concrete_nouns.txt')


def random_phone_number():
    """Generates a random 10 digit phone number that does not start with 0."""
    return random.randint(100_000_0000, 1_000_000_0000)


def random_name():
    """Generates a random (First Name, Last Name) tuple."""
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def random_email(name_tuple):
    """Generates a first_last@random.com email address from a name."""
    return f"{name_tuple[0]}_{name_tuple[1]}@random.com"


NUM_SUFFIXES = ['th', 'st', 'nd', 'rd'] + ['th'] * 6
ADDRESS_FORMAT = "%d %d%s %s, %s %d"


def random_address():
    """Generates a random street address in a simple format."""
    num_1 = random.randint(1, 10000)
    num_2 = random.randint(1, 1000)
    street = random.choice(("St.", "Ave."))
    city = random.choice(CITY_STATES)
    zcode = random.randint(10_000, 100_000)
    return ADDRESS_FORMAT % (num_1, num_2, NUM_SUFFIXES[num_2 % 10], street,
                             city, zcode)


def random_customer(cid):
    """Randomly generates a complete customer with name + contact info."""
    customer = dict()
    customer_name_tuple = random_name()
    customer['first_name'], customer['last_name'] = customer_name_tuple
    customer['address'] = random_address()
    customer['phone'] = random_phone_number()
    customer['email'] = random_email(customer_name_tuple)
    customer['customer_id'] = f'user{cid:04d}'
    return customer


def random_product(prod_id):
    """Create a product with the given id and a random quantity."""
    product = dict()
    product['product_id'] = f'prd{prod_id:04d}'
    product['description'] = CONCRETE_NOUNS[prod_id % len(CONCRETE_NOUNS)]
    product['product_type'] = CONCRETE_NOUNS[prod_id % len(CONCRETE_NOUNS)]
    product['quantity_available'] = random.choice([0, 1, 3, 10])
    return product


def write_csv(data, filename):
    """Write the data to csv with the given filename."""
    keys = data[0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def do_generation(n_cust, n_prod, n_rent, *, suffix=''):
    """Generate random data of custom sample size.s"""
    # Generate customers CSV
    customers = [random_customer(i) for i in range(n_cust)]
    write_csv(customers, f'customers{suffix}.csv')

    # Generate products CSV
    products = [random_product(i) for i in range(n_prod)]
    write_csv(products, f'products{suffix}.csv')

    # Generate rentals CSV
    rentals = list()
    for i in range(n_rent):
        rental = dict()
        rental['rental_id'] = f'rnt{i:05d}'
        rental['customer_id'] = random.choice(customers)['customer_id']
        rental['product_id'] = random.choice(products)['product_id']
        rentals.append(rental)
    write_csv(rentals, f'rentals{suffix}.csv')


if __name__ == "__main__":
    # SMALL FILES
    do_generation(1000, 1000, 1000, suffix='_small')
    # MEDIUM FILES
    do_generation(10_000, 10_000, 10_000, suffix='_med')
    # LARGE FILES
    do_generation(100_000, 100_000, 100_000, suffix='_large')
