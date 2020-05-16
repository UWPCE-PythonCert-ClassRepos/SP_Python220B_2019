"""
Module for diagnosis for linear versus parallel.
"""

#pylint:disable=invalid-name

from linear import import_data_linear
from parallel import import_data_parallel

# Set up args
directory = 'data'
product_file = 'product_data.csv'
customer_file = 'customer_data.csv'
rental_file = 'rental_data.csv'

def run_linear_import():
    """Run linear importation method."""

    import_data_linear(directory, product_file,
                       customer_file, rental_file)

def run_parallel_import():
    """Run parallel importation method."""

    import_data_parallel(directory, product_file,
                         customer_file, rental_file)


if __name__ == '__main__':
    # Run methods of importation
    run_linear_import()
    run_parallel_import()
