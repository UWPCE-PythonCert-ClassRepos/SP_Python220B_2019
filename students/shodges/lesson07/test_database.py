from unittest import TestCase

import parallel
import linear

class RentalDbTest(TestCase):
    """
    Tests for population and data integrity of database.
    """
    def test_1_import(self):
        """
        Test that the records are successfully imported.
        """
        # Start fresh so we don't mess up all our tests...
        linear.drop_data()
        self.assertEqual(linear.show_available_products(), {})

        # Check for proper error handling of import_data()
        with self.assertRaises(FileNotFoundError):
            result = linear.import_data('data2', 'p.csv', 'c.csv', 'r.csv')

        # These tests are hard-coded to the expected values from the incluced CSV's.
        # Your results may vary if the data sets change. :)
        result = linear.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(result[0][0], 1000)
        self.assertEqual(result[0][1], 0)
        self.assertEqual(result[0][2], 1000)
        self.assertEqual(result[1][0], 1000)
        self.assertEqual(result[1][1], 0)
        self.assertEqual(result[1][2], 1000)

        linear_available = linear.show_available_products()

        # Run the parallel again -- we're going to grab the results of show_available_products()
        # to consistency check later.
        parallel.drop_data()
        self.assertEqual(parallel.show_available_products(), {})

        with self.assertRaises(FileNotFoundError):
            result = linear.import_data('data2', 'p.csv', 'c.csv', 'r.csv')

        result = parallel.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(result[0][0], 1000)
        self.assertEqual(result[0][1], 0)
        self.assertEqual(result[0][2], 1000)
        self.assertEqual(result[1][0], 1000)
        self.assertEqual(result[1][1], 0)
        self.assertEqual(result[1][2], 1000)

        self.assertEqual(linear_available, parallel.show_available_products())

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

    def test_3_show_rentals(self):
        """
        Test the integrity of the returned dictionary of active rentals.
        """

        cust_1 = {'name': 'George Washington',
                  'address': '4 Bowling Green',
                  'phone_number': '2125555555',
                  'email': 'george@governmenthouse.com'}

        cust_2 = {'name': 'John Adams',
                  'address': '524-30 Market St',
                  'phone_number': '2675551212',
                  'email': 'john@presidentshouse.com'}

        cust_3 = {'name': 'Thomas Jefferson',
                  'address': '1600 Pennsylvania Ave',
                  'phone_number': '2029999999',
                  'email': 'thomas@whitehouse.gov'}

        result = database.show_rentals('SOFA')
        self.assertEqual(len(result), 2)
        self.assertEqual(result['cust_1'], cust_1)
        self.assertEqual(result['cust_3'], cust_3)

        result = database.show_rentals('RECLINER')
        self.assertEqual(len(result), 0)

        result = database.show_rentals('DININGTABLE')
        self.assertEqual(len(result), 3)
        self.assertEqual(result['cust_1'], cust_1)
        self.assertEqual(result['cust_2'], cust_2)
        self.assertEqual(result['cust_3'], cust_3)

        result = database.show_rentals('OVEN')
        self.assertEqual(len(result), 2)
        self.assertEqual(result['cust_2'], cust_2)
        self.assertEqual(result['cust_3'], cust_3)

        result = database.show_rentals('MOPED')
        self.assertEqual(len(result), 1)
        self.assertEqual(result['cust_3'], cust_3)

        result = database.show_rentals('FUTON') # Validate an empty dict is received
        self.assertEqual(result, {})
