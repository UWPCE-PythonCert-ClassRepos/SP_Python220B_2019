
"""
expand_data.py
Assignment 7
Joli Umetsu
PY220
"""

import random
from csv import reader, writer


def get_data(filename):
    """
    Gets data from csv file
    Returns: List
    """
    with open(filename, newline='') as file:
        data = reader(file, delimiter=',')
        return [[line.strip().title() for line in row] for row in data]


def create_cust_data(entries, firstnames, lastnames, streets):
    """
    Generates random customer data
    Returns: List
    """
    customer_info = []
    street_type = ('St', 'Ave', 'Blvd', 'Pl', 'Way', 'Dr')
    street_ext = ("", "", 'N', 'S', 'E', 'W', 'NE', 'SW', 'NW', 'SE')
    area_code = (206, 253, 360, 425, 509, 564, 503, 541)
    email_provider = ('gmail', 'hotmail', 'yahoo', 'aol', 'outlook', 'icloud')

    for i in range(1, entries+1):
        user_id = "user" + "{:04d}".format(i)
        first_name = random.choice(firstnames)
        last_name = random.choice(lastnames)
        name = first_name + " " + last_name
        street_number = str(random.randrange(1, 9, 1)) + \
                        "".join(["{}".format(random.randint(0, 9)) for num in range(0, 3)])
        street_name = random.choice(streets) + " " + random.choice(street_type) + \
                      " " + random.choice(street_ext)
        address = street_number + " " + street_name
        phone_number = str(random.choice(area_code)) + \
                       "".join(["{}".format(random.randint(0, 9)) for num in range(0, 7)])
        email = first_name + last_name + "@" + random.choice(email_provider) + ".com"
        customer_info.append([user_id, name, address, phone_number, email])

    return customer_info


def create_prod_data(entries):
    """
    Generates random product data
    Returns: List
    """
    product_info = []
    prod_types = ('livingroom', 'kitchen', 'bedroom')
    items = ('TV stand', 'L-shaped sofa', 'Sofa', 'Bar stool', 'Stool', 'Bed frame', 'Desk',
             'End table', 'Coffee table', 'Book shelf', 'Dresser', 'Dining table', 'Stand')
    sizes = ('S', 'M', 'L', 'XL')
    colors = ('black', 'white', 'silver', 'gold', 'brown', 'blue', 'green', 'red', 'purple',
              'bronze')
    finishes = ('gold', 'platinum', 'lacquer', 'chrome', 'varnish', 'resin', 'oil', 'paint',
                'wood', 'bare', 'silver', 'diamonds')

    for i in range(1, entries+1):
        prod_id = "prod" + "{:04d}".format(i)
        description = random.choice(items) + "; size: " + random.choice(sizes) + ", color: " \
                      + random.choice(colors) + ", finish: " + random.choice(finishes)
        prod_type = random.choice(prod_types)
        available = random.randrange(0, 30, 1)
        product_info.append([prod_id, description, prod_type, available])

    return product_info


# def create_rent_data(n, customerinfo, productinfo):
#     """
#     Generates random rental data
#     Returns: List
#     """
#     rental_info = []

#     for i in range(1, n+1):
#         prod_id = random.choice(productinfo)[0]
#         quantity = random.choice(range(1,5))
#         user_id = random.choice(customerinfo)[0]
#         rental_info.append([prod_id, quantity, user_id])

#     return rental_info


def write_data(filename, data):
    """
    Writes data to csv file
    """
    header = {'customers': ['user_id', 'name', 'address', 'phone', 'email'],
              'products': ['prod_id', 'description', 'prod_type', 'qty_avail']}

    with open(filename, 'w', newline='') as file:
        f_writer = writer(file)
        f_writer.writerow(header[filename[6:-4]])
        for line in data:
            f_writer.writerow(line)


def main():
    """
    Main program
    """
    n_entries = 1000

    # get data from files
    fname_data = get_data('files/data/first_names.csv')
    lname_data = get_data('files/data/last_names.csv')
    street_data = get_data('files/data/street_names.csv')

    # flatten the list of data
    first_names = [item for element in fname_data for item in element]
    last_names = [item for element in lname_data for item in element]
    street_names = [item for element in street_data for item in element]

    # generate customer data and write to file
    customer_info = create_cust_data(n_entries, first_names, last_names, street_names)

    # generate product data and write to file
    product_info = create_prod_data(n_entries)

    # generate rental data
    # rental_info = create_rent_data(n_entries, customer_info, product_info)

    # write data to file
    write_data('files/customers.csv', customer_info)
    write_data('files/products.csv', product_info)
    # write_data('files/rentals.csv', rental_info)


if __name__ == "__main__":
    main()
