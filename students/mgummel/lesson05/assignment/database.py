"""Database module for Customer and product information"""
import json

from os import path
from pymongo import MongoClient
import pandas



#pylint diasbled errors: too-many-locals



class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """

    :param directory_name: Directory to find files in
    :param product_file: Product information in csv
    :param customer_file: Customer Information in csv
    :param rentals_file: Rental information in csv
    :return:
    """
    documents = list()
    num_of_errors = list()

    file_list = list()
    file_list.append({"products": path.join(directory_name, product_file)})
    file_list.append({"customers": path.join(directory_name, customer_file)})
    file_list.append({"rentals": path.join(directory_name, rentals_file)})

    client = MongoDBConnection()

    with client:
        database = client.connection.HPNorton

        for key_value in file_list:
            for key, value in key_value.items():
                error_count = 0

                try:
                    csv_reader = pandas.read_csv(filepath_or_buffer=value, error_bad_lines=False)
                    data_json = json.loads(csv_reader.to_json(orient='records'))

                    for row in data_json:
                        database[key].insert_one(row)
                    documents.append(csv_reader.shape[0])

                except FileNotFoundError as error:
                    print(f"{error}")
                    error_count += 1
                    documents.append(0)

                num_of_errors.append(error_count)

    return tuple(documents), tuple(num_of_errors)


def calculate_rows(filename):
    """
    Calculates the number of rows in aafile
    :param filename: Name of the file to calculate rows for
    :return: Number of lines minus 1
    """
    with open(filename, 'r') as file_rows:
        lines = len(file_rows.readlines())
    return lines - 1


def show_available_products():
    """
    Show all available products fields with information
    :return: a dictionary of all products that are avialable
    """
    all_products = dict()
    product_client = MongoDBConnection()

    with product_client:
        database = product_client.connection.HPNorton

        for product in database.products.find({"quantity_available":{"$gt": 0}}):
            product_dict = dict()
            product_dict["quantity_available"] = product["quantity_available"]
            product_dict["description"] = product["description"]
            product_dict["product_type"] = product["product_type"]
            all_products[product["product_id"]] = product_dict

    return all_products


def show_rentals(product_id):
    """
    Show all customers that have rented a product based on the
    product id
    :param product_id: product id for rental item
    :return: All customer information for those that have rented
    the product
    """
    all_customers = dict()
    renter_list = list()
    rental_client = MongoDBConnection()

    with rental_client:

        database = rental_client.connection.HPNorton
        for rental in database.rentals.find({'product_id': product_id}):
            renter_list.append(rental["user_id"])

        for uid in renter_list:
            for customer in database.customers.find({"user_id":{"$eq": uid}}):
                customer_dict = dict()
                customer_dict["name"] = customer["name"]
                customer_dict["address"] = customer["address"]
                customer_dict["email"] = customer["email"]
                customer_dict["phone_number"] = customer["phone_number"]
                all_customers[customer["user_id"]] = customer_dict

    return all_customers



def main():
    """
    Main function to call methods for determining functional testing.
    :return: N/A
    """
    import_data(".", 'products.csv', 'customer.csv', 'rentals.csv')
    show_available_products()
    print(show_rentals(7298))



if __name__ == '__main__':
    main()
