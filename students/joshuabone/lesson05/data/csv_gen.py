"""Functions for generating fake CSV data."""
import csv
import random

N_CUSTOMERS = 10_000
N_RENTALS = 100_000


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


def build_product(prod_id):
    """Create a product with the given id and a random quantity."""
    product = dict()
    product['product_id'] = f'prd{prod_id:04d}'
    product['description'] = CONCRETE_NOUNS[prod_id]
    product['product_type'] = CONCRETE_NOUNS[prod_id]
    product['quantity_available'] = random.choice([0, 1, 3, 10])
    return product


def write_csv(data, filename):
    """Write the data to csv with the given filename."""
    keys = data[0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == "__main__":
    # Generate customers CSV
    CUSTOMERS = [random_customer(i) for i in range(N_CUSTOMERS)]
    write_csv(CUSTOMERS, 'customers.csv')

    # Generate products CSV
    PRODUCTS = [build_product(i) for i in range(len(CONCRETE_NOUNS))]
    write_csv(PRODUCTS, 'products.csv')

    # Generate rentals CSV
    RENTALS = list()
    for i in range(N_RENTALS):
        rental = dict()
        rental['rental_id'] = f'rnt{i:05d}'
        rental['customer_id'] = random.choice(CUSTOMERS)['customer_id']
        rental['product_id'] = random.choice(PRODUCTS)['product_id']
        RENTALS.append(rental)
    write_csv(RENTALS, 'rentals.csv')
