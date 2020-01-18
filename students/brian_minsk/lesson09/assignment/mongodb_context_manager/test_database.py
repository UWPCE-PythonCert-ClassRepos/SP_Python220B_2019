""" Tests for the lesson05 assignment.

Note: The tests are intimately associated with the data in the csv files for this assignment since
they sometimes test for particular values.
"""

# pylint: disable=unused-variable

from unittest import TestCase
import logging
import sys
import database as db

sys.path.append('C:\\Users\\brian\\PythonClass\\PY220\\SP_Python220B_2019\\'
                '\\students\\brian_minsk\\lesson05\\assignment')

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class PrePopulatedTests(TestCase):
    """ Tests run before data is added to the db.
    """
    def tearDown(self):
        """ Clear out the MongoDB collections.
        """
        db.PRODUCT_COLLECTION.drop()
        db.CUSTOMER_COLLECTION.drop()
        db.RENTAL_COLLECTION.drop()

    def test_import_data_record_count(self):
        """ Read in one the 3 csv files and check that the record count returned for products,
        customers, and rentals is correct.
        """
        record_counts, error_counts = db.import_data("csv_files",
                                                     "product.csv",
                                                     "customers.csv",
                                                     "rentals.csv")

        self.assertTupleEqual(record_counts, (5, 3, 10))

    def test_import_data_error_count(self):
        """ Read in the 3 csv files and check that the error count returned is zero for all of
        them.
        """
        record_counts, error_counts = db.import_data("csv_files",
                                                     "product.csv",
                                                     "customers.csv",
                                                     "rentals.csv")

        self.assertTupleEqual(error_counts, (0, 0, 0))

    def test_import_data_bad_data_error_count(self):
        """ Read in the 3 csv files wit bad data and check that the error count returned is
        correct for all of them.
        """
        record_counts, error_counts = db.import_data("csv_files",
                                                     "product_bad.csv",
                                                     "customers_bad.csv",
                                                     "rentals_bad.csv")

        self.assertTupleEqual(error_counts, (1, 1, 2))


class PostPopulatedTest(TestCase):
    """ Tests run after data sample is added to the db.
    """
    def setUp(self):
        """ Clear out the MongoDB db if it exists then populate with the data from the csv files.
        """
        db.import_data("csv_files", "product.csv", "customers.csv", "rentals.csv")

    def tearDown(self):
        """ Clear out the MongoDB collections.
        """
        db.PRODUCT_COLLECTION.drop()
        db.CUSTOMER_COLLECTION.drop()
        db.RENTAL_COLLECTION.drop()

    def test_show_available_product(self):
        """ Test that the dictionary of available products returned is correct.
        """
        available_products = db.show_available_products()

        test_dict = {1: {'description': 'violet fuzzy velvet sofa',
                         'type': 'livingroom',
                         'quantity_available': 43},
                     2: {'description': 'that leg lamp from Christmas Story',
                         'type': 'lighting',
                         'quantity_available': 55},
                     3: {'description': 'giant psychedelic lava lamp',
                         'type': 'lighting',
                         'quantity_available': 234},
                     5: {'description': 'rotating pink water bed',
                         'type': 'bedroom',
                         'quantity_available': 2}}

        self.assertDictEqual(available_products, test_dict)

    def test_show_rentals(self):
        """ Test that the dictionary of rentals returned is correct.
        """
        rentals = db.show_rentals(4)

        test_dict = {2: {'name': 'Shady Flava',
                         'address': '987 Elm Street, Elsewhere, CA 09876',
                         'phone': '999.888.7777',
                         'email_address': 'shady.flava@gmail.com'},
                     3: {'name': 'Vegeta Colt',
                         'address': '5554 Oak Lane, Nowhere, ND, 50000',
                         'phone': '555.444.6666',
                         'email_address': 'vegeta.colt@gmail.com'}}

        self.assertDictEqual(rentals, test_dict)
