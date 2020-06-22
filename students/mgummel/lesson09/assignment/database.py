"""Database module for Customer and product information"""

from contxt_mgr import *
from os import path
import pandas



#pylint diasbled errors: too-many-locals


def import_data(directory_name, product_file, customer_file, rentals_file):
    """

    :param directory_name: Directory to find files in
    :param product_file: Product information in csv
    :param customer_file: Customer Information in csv
    :param rentals_file: Rental information in csv
    :return:
    """

    file_list = list()
    file_list.append({"products": path.join(directory_name, product_file)})
    file_list.append({"customers": path.join(directory_name, customer_file)})
    file_list.append({"rentals": path.join(directory_name, rentals_file)})

    data_import = DataImport()

    with data_import as di:
        results = di.write_to_mongo(file_list)

    return results


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
    product_manager = Products()

    with product_manager as pm:
        available_products = pm.get_available_products()

    return available_products


def show_rentals(product_id):
    """
    Show all customers that have rented a product based on the
    product id
    :param product_id: product id for rental item
    :return: All customer information for those that have rented
    the product
    """
    rental_manager = Renter()

    with rental_manager as rm:
        customer_info = rm.match_customers(product_id)

    return customer_info



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
