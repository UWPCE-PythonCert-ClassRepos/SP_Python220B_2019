"""Module for running multiple conditions for timing testing on database.py"""
from database import import_data, show_available_products, show_rentals

TEST_DIRECTORY = 'tests/test_files'

if __name__ == "__main__":
    import_data(TEST_DIRECTORY, 'products_small.csv', 'customers_small.csv', 'rentals_small.csv')
    show_available_products()
    show_rentals('A-3')
    import_data(TEST_DIRECTORY, 'products_med.csv', 'customers_med.csv', 'rentals_med.csv')
    show_available_products()
    show_rentals('A-3')
    import_data(TEST_DIRECTORY, 'products_large.csv', 'customers_large.csv', 'rentals_large.csv')
    show_available_products()
    show_rentals('A-3')
