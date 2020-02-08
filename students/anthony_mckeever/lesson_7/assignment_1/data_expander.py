# Advanced Programming In Python - Lesson 7 Assignment 1:
#                                  Threading & Concurrency
# RedMine Issue - SchoolOps-17
# Code Poet: Anthony McKeever
# Start Date: 01/10/2020
# End Date: 01/11/2020

"""
Expand the data of the MongoDB Input Files

Files Touched:
    data/products.csv
    data/customers.csv
    data/rentals.csv
"""

import random
import threading

FIRST_NAMES = ["Cresenta", "Astra", "Delilah", "Kima", "Kayomi", "Katie",
               "Jelissa", "Mayrina", "Yolanda", "Marisol", "Vivian", "Galaxia",
               "Andromeda", "Stella", "Harmony", "Melody", "Sophia", "Lynn",
               "Lauren", "Arielle", "Nermina", "Valery", "Amy", "Jam", "Abby"]

LAST_NAMES = ["McKeever", "Starchelle", "Matsuka", "Matsume", "Metoyo", "Star",
              "Sivertsen", "Ramirez", "Starchilly", "Jelly", "Avdic", "Lien",
              "McNerney", "Lu", "Oak", "Elm", "Burch", "Rowan", "Juniper",
              "Sycamore", "Kukui", "Magnolia", "Sunflower", "Rose", "Lovelle"]

STREETS = ["Starshine", "Limelight", "Cinnamon", "Strawberry", "Cherry", "Way",
           "Lime", "Apple", "Moonlight", "Starlight", "Nutmeg", "Cherrish",
           "Alpaca", "Goat", "Sheep", "Llama", "Bear", "Loaf", "Taco", "Almia",
           "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]

STREET_TYPE = ["Dr.", "Rd.", "St.", "Blvd", "Ave", "Crest", "Ln.", "Ct."]

CITIES = ["Pallet Town", "New Sophiesville", "Sophiesville", "Misty Autumn",
          "Neverwinter", "Maybespring", "Alwayssummer", "Sometimesautumn",
          "Solstice", "Equinox", "Collette", "Petunia", "Foxglove", "Daisy"]

EMAIL_DOMAINS = ["com.com", "com.net", "com.org", "net.com", "net.net",
                 "net.org", "org.com", "org.net", "org.org", "com.net.org"]

STATES = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
          'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
          'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NA', 'NC', 'ND',
          'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR',
          'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI',
          'WV', 'WY']

LIST_CUSTOMER_IDS = []
LIST_PRODUCT_IDS = []


def get_customer(id_number):
    """
    Return a new randomized customer

    :id_number: An integer representing the customer's number.
    """
    cust_id = f"user{id_number:04}"
    LIST_CUSTOMER_IDS.append(cust_id)
    first_name = FIRST_NAMES[random.randint(0, len(FIRST_NAMES) - 1)]
    last_name = LAST_NAMES[random.randint(0, len(LAST_NAMES) - 1)]

    street = STREETS[random.randint(0, len(STREETS) - 1)]
    street = f"{street} {STREET_TYPE[random.randint(0, len(STREET_TYPE) - 1)]}"
    street = f"{random.randint(0, 9999)} {street}"
    street = f"{street} {CITIES[random.randint(0, len(CITIES) - 1)]}"
    street = f"{street} {STATES[random.randint(0, len(STATES) - 1)]}"
    street = f"{street} {random.randint(10000, 99999)}"

    email = EMAIL_DOMAINS[random.randint(0, len(EMAIL_DOMAINS) - 1)]
    email = f"{first_name[:random.randint(1, 10)]}.{last_name}@{email}"

    phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}"
    phone = f"{phone}-{random.randint(1000, 9999)}"

    return f"\n{cust_id},{first_name} {last_name},{street},{phone},{email}"


def get_product():
    """
    Return a randomized product.
    """
    list_lists = [FIRST_NAMES, LAST_NAMES, STREETS, CITIES]
    product_name = ""
    product_desc = ""
    product_id = ""

    for __ in range(random.randint(1, 3)):
        index_a = random.randint(0, len(list_lists) - 1)
        index_b = random.randint(0, len(list_lists[index_a]) - 1)
        product_name = f"{product_name} {list_lists[index_a][index_b]}"

    for __ in range(random.randint(3, 10)):
        index_a = random.randint(0, len(list_lists) - 1)
        index_b = random.randint(0, len(list_lists[index_a]) - 1)
        product_desc = f"{product_desc} {list_lists[index_a][index_b]}"

    for name in product_name.split(" "):
        product_id = f"{product_id}{name[:1].upper()}"

    while True:
        id_number = random.randint(100, 999999)

        if f"{product_id}_{id_number}" not in LIST_PRODUCT_IDS:
            product_id = f"{product_id}_{id_number}"
            LIST_PRODUCT_IDS.append(product_id)
            break

    product_name = product_name.strip()
    product_desc = product_desc.strip()
    quantity = random.randint(0, 1000)

    return f"\n{product_id},{product_name},{product_desc},{quantity}"


def get_rental(number):
    """
    Return a randomized rental.

    :number:    An integer representing the number of the rental.
    """
    rental_id = f"rental_{number:04}"
    customer = LIST_CUSTOMER_IDS[random.randint(0, len(LIST_CUSTOMER_IDS) - 1)]
    product = LIST_PRODUCT_IDS[random.randint(0, len(LIST_PRODUCT_IDS) - 1)]

    return f"\n{rental_id},{customer},{product}"


def get_file_length(file_name):
    """
    Return the length of a file.

    :file_name: The path and name of the file.
    """
    # Subtract 1 to ignore header
    return sum(1 for line in open(file_name))


def expand_file(file_name, get_method, takes_int):
    """
    Expands the data in a given file.

    :file_name: The path and name of the file.
    :get_method:    The method to use for generating data.
    :takes_int:     Whether or not the get_method takes an integer parameter.
                    Conditions:
                        True = get_method uses the integer parameter.
                        False = get_method does not use the integer parameter.
    """
    current_len = get_file_length(file_name)

    with open(file_name, "a+") as write_file:
        for i in range(current_len, 1001):
            if takes_int:
                write_file.write(get_method(i))
            else:
                write_file.write(get_method())


def expand_data():
    """
    Expands the data in products.csv, customers.csv, and rentals.csv
    """
    products_file = "data/products.csv"
    prod_args = (products_file, get_product, False)

    product_thread = threading.Thread(target=expand_file, args=prod_args)
    product_thread.daemon = True
    product_thread.start()

    customers_file = "data/customers.csv"
    customers_args = (customers_file, get_customer, True)

    customer_thread = threading.Thread(target=expand_file, args=customers_args)
    customer_thread.daemon = True
    customer_thread.start()

    product_thread.join()
    customer_thread.join()

    expand_file("data/rentals.csv", get_rental, True)


def main():
    """
    The main method of the app.
    """
    expand_data()


if __name__ == "__main__":
    main()
