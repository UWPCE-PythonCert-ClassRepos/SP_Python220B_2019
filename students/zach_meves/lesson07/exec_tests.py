"""
Generic test suite.
"""

import unittest
import os
import csv
from unittest import mock

import sys
args = sys.argv[1:]

# Import linear or parallel depending on arguments given
if args[-1] == "linear":
    import linear
    database = linear
    NAME = "linear"
elif args[-1] == "parallel":
    import parallel
    database = parallel
    NAME = "parallel"
else:
    sys.stderr("Must provide either 'linear' or 'parallel'")
    sys.exit(-1)


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

# Test CSV files
CUSTOMERS = 'customers.csv'
PRODUCTS = 'products.csv'
RENTALS = 'rentals.csv'

# Test CSV field names
USER_ID, USER_NAME = "user_id", "name"
USER_ADDRESS, USER_EMAIL = "address", "email"
USER_PHONE = "phone_number"

PROD_ID, PROD_DESC = "product_id", "description"
PROD_TYPE, PROD_QTY = "product_type", "quantity"

RENT_QTY = "quantity_rented"
PROD_REMAIN = "quantity_available"


class TestCsvIO(unittest.TestCase):
    """Test reading/writing of CSV files"""

    def setUp(self) -> None:
        """Set up test case"""

        self.header = ('A', 'b', 'Cd')
        self.entries = ((1, 'a', 'd'),
                        (2, 'b', 'e'),
                        (3, 'c', 'f'))

        self.data_list = [dict(zip(self.header, entry)) for entry in self.entries]
        self.data_dict = dict(zip((entry[0] for entry in self.entries), self.data_list))

        self.filename = "test_file.csv"

        # Export CSV
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.entries)

    def test_read_list(self):
        """Test reading CSV with list output"""

        # Read the file and assert that the dictionary output
        # matches self.data_list
        data = database.read_csv(self.filename)

        self.assertEqual(self.data_list, data)

    def test_read_dict(self):
        """Test reading CSV with dict output"""

        # Read the file and assert that the dictionary output
        # matches self.data_dict
        data = database.read_csv(self.filename, keyed=True)

        self.assertEqual(self.data_dict, data)

    def tearDown(self) -> None:
        """Remove test file"""

        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass


@mock.patch(f'{NAME}.DB_NAME', 'test_db')
class TestDatabase(unittest.TestCase):
    """Test cases for database"""

    @mock.patch(f'{NAME}.DB_NAME', 'test_db')
    def setUp(self) -> None:
        """Set up test case"""

        # The read_csv method is tested above
        self.customer_data = database.read_csv(os.path.join(DATA_DIR, CUSTOMERS), keyed=True)
        self.product_data = database.read_csv(os.path.join(DATA_DIR, PRODUCTS), keyed=True)
        self.rental_data = database.read_csv(os.path.join(DATA_DIR, RENTALS), keyed=False)

        self.customer_keys = list(self.customer_data.keys())
        self.product_keys = list(self.product_data.keys())

        self.products_remaining = dict(zip(self.product_keys,
                                           (self.product_data[k][PROD_QTY] for
                                            k in self.product_keys)))

        for rental in self.rental_data:  # Subtract rented quantities from stock
            prod, qty = rental[PROD_ID], rental[RENT_QTY]
            try:
                self.products_remaining[prod] = self.products_remaining[prod] - qty
            except KeyError:
                pass
            else:
                if self.products_remaining[prod] <= 0:
                    self.products_remaining.pop(prod)

    @mock.patch(f'{NAME}.DB_NAME', 'test_db')
    def tearDown(self) -> None:
        """
        Remove database data.

        .. note::
            For some reason, the patch decorators on the class
            DO NOT get applied to ``setUp`` or ``tearDown``.
        """

        with database.MongoManager() as mm:

            mm.db.product.delete_many({})
            mm.db.customers.delete_many({})
            mm.db.rentals.delete_many({})

            for name in ('products', 'customers', 'rentals'):
                mm.db.drop_collection(name)

    def test_import_data(self):
        """Test database.import_data"""

        database.import_data(DATA_DIR, PRODUCTS, CUSTOMERS, RENTALS)

        # Order = products, customers, rentals
        # names = ("Products", "Customers", "Rentals")
        # n_prod = len(self.product_keys)
        # n_cust = len(self.customer_keys)
        # n_rent = len(self.rental_data)
        #
        # for correct, value, name in zip((n_prod, n_cust, n_rent), success, names):
        #     self.assertEqual(correct, value, name)
        #
        # self.assertEqual((0, 0, 0), fail, "Fail count")

        # Assert they were added to the database correctly
        with database.MongoManager() as mm:
            self.assertEqual(len(self.rental_data), mm.db.rentals.count_documents({}), "Rental count")
            self.assertEqual(len(self.product_keys), mm.db.products.count_documents({}), "Prod count")
            self.assertEqual(len(self.customer_keys), mm.db.customers.count_documents({}), "Cust count")

    def test_show_available_products(self):
        """Test database.show_available_products"""

        self.assertEqual({}, database.show_available_products(), "Nothing so far")

        database.import_data(DATA_DIR, PRODUCTS, CUSTOMERS, RENTALS)

        prods_to_show = database.show_available_products()
        correct = dict(zip(prods_to_show, ({PROD_DESC: self.product_data[prod][PROD_DESC],
                                            PROD_TYPE: self.product_data[prod][PROD_TYPE],
                                            PROD_REMAIN: self.products_remaining[prod]}
                                           for prod in prods_to_show)))

        self.assertEqual(correct, prods_to_show, "Products to show")

    def test_show_rentals(self):
        """Test database.show_rentals"""

        database.import_data(DATA_DIR, PRODUCTS, CUSTOMERS, RENTALS)

        if "prodX" not in self.product_data:
            self.assertEqual({}, database.show_rentals("prodX"))
        else:
            raise NameError("Test case invalid - 'prodX' exists as a product key")

        # Compute correct rental data
        for product in self.product_keys:
            correct = {}
            for entry in self.rental_data:
                user, prod, qty = entry[USER_ID], entry[PROD_ID], entry[RENT_QTY]
                if prod == product:  # Add as rental for this product
                    correct[user] = self.customer_data[user]
                    try:
                        correct[user].pop(USER_ID)
                    except KeyError:
                        pass

            self.assertEqual(correct, database.show_rentals(product))

    def test_show_products_for_customer(self):
        """Tests database.show_products_for_customer"""

        database.import_data(DATA_DIR, PRODUCTS, CUSTOMERS, RENTALS)

        correct = []
        for key in sorted(self.products_remaining):
            correct.append({PROD_DESC: self.product_data[key][PROD_DESC],
                            PROD_TYPE: self.product_data[key][PROD_TYPE],
                            'quantity_available': self.products_remaining[key]})
        self.assertEqual(correct,
                         database.show_products_for_customer())


if __name__ == "__main__":
    print("main...")
    unittest.main()
