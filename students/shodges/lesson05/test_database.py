from unittest import TestCase

import database

class RentalDbTest(TestCase):
    """
    Tests for population and data integrity of database.
    """
    def test_1_import(self):
        """
        Test that the records are successfully imported.
        """
        # Start fresh so we don't mess up all our tests...
        database.drop_data()

        # These tests are hard-coded to the expected values from the incluced CSV's.
        # Your results may vary if the data sets change. :)
        result = database.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(result[0][0], 5) # Number of records added from products.csv
        self.assertEqual(result[0][1], 3) # Number of records added from customers.csv
        self.assertEqual(result[0][2], 8) # Number of records added from rentals.csv
        self.assertEqual(result[1][0], 0) # No errors found

    def test_2_show_available(self):
        """
        Test the integrity of the returned dictionary of available products.  We particularly
        want to validate that quantity_available is deducted to account for existing rentals.
        """
        result = database.show_available_products()
        self.assertEqual(result['SOFA']['quantity_available'], 16)
        self.assertEqual(result['RECLINER']['quantity_available'], 0)
        self.assertEqual(result['DININGTABLE']['quantity_available'], 7)
        self.assertEqual(result['OVEN']['quantity_available'], 4)
        self.assertEqual(result['MOPED']['quantity_available'], 0)
