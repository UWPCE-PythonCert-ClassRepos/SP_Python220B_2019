"""A context manager module that controls access to a MongoDB"""
import json
import pandas
from pymongo import MongoClient


class Products():
    """
    A Context Manager that reads from a MongoDB. The main function of this
    class is to get all products from a MongoDB that are not sold out.
    Meaning num of products > 0.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self


    def get_available_products(self):
        """
        Show all available products fields with information
        :return: a dictionary of all products that are available
        """

        all_products = dict()
        database = self.connection.HPNorton

        for product in database.products.find({"quantity_available":{"$gt": 0}}):
            product_dict = dict()
            product_dict["quantity_available"] = product["quantity_available"]
            product_dict["description"] = product["description"]
            product_dict["product_type"] = product["product_type"]
            all_products[product["product_id"]] = product_dict

        return all_products


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()



class Renter():
    """
    A Context Manager that reads from a MongoDB. The main function of this
    class determines which product has been rented by which customer.
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self


    def match_customers(self, p_id):
        """
        Determines which customers rented the product based
        on the product ID parameter.

        :param p_id: product id
        :return: customer info for renters of the p_id
        """
        all_customers = dict()
        renter_list = list()

        database = self.connection.HPNorton
        for rental in database.rentals.find({'product_id': p_id}):
            renter_list.append(rental["user_id"])

        for uid in renter_list:
            for customer in database.customers.find({"user_id": {"$eq": uid}}):
                customer_dict = dict()
                customer_dict["name"] = customer["name"]
                customer_dict["address"] = customer["address"]
                customer_dict["email"] = customer["email"]
                customer_dict["phone_number"] = customer["phone_number"]
                all_customers[customer["user_id"]] = customer_dict

        return all_customers

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()



class DataImport():
    """
    A Context Manager that populates a MongoDB. The main function of this
    takes a list of files and writes their values to a MongoDB.
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None


    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self


    def write_to_mongo(self, files_to_import):
        """
        Takes a list of files, parses each file line-by-line and
        writes the data to the Mongodb
        :param files_to_import: list of files to parse and write
        :return: Tuple containing number of entries for each file and num of errors
        """

        docs = list()
        errors = list()
        database = self.connection.HPNorton

        for key_value in files_to_import:
            for key, value in key_value.items():
                error_count = 0

                try:
                    csv_reader = pandas.read_csv(filepath_or_buffer=value, error_bad_lines=False)
                    data_json = json.loads(csv_reader.to_json(orient='records'))

                    for row in data_json:
                        database[key].insert_one(row)
                    docs.append(csv_reader.shape[0])

                except FileNotFoundError as error:
                    print(f"{error}")
                    error_count += 1
                    docs.append(0)

                errors.append(error_count)

        return tuple(docs), tuple(errors)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
