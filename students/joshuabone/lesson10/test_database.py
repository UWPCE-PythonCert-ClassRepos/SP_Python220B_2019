"""Unit tests for the Mongo DB backend of the rentals app."""
import unittest
import database as db


class MongoTests(unittest.TestCase):
    """Unit tests for the Mongo DB backend of the rentals app."""
    def setUp(self):
        mongo = db.MongoDBConnection()
        with mongo:
            db.DATABASE = mongo.connection.test_rentals
            db.drop_data()

    def test_show_available_products_works(self):
        """Test that we can retrieve all available products."""
        products = [
            {'product_id': 'prd0000', 'description': 'Gum',
             'product_type': 'Candy', 'quantity_available': '5'},
            {'product_id': 'prd0001', 'description': 'Atomic Fireball',
             'product_type': 'Candy', 'quantity_available': '0'},
            {'product_id': 'prd0002', 'description': 'Mello Yellow',
             'product_type': 'Soda', 'quantity_available': '10'}
        ]
        db.DATABASE['product'].insert_many(products)

        available = db.show_available_products()
        self.assertEqual(available,
                         {'prd0000': {'description': 'Gum',
                                      'product_type':'Candy',
                                      'quantity_available': 5},
                          'prd0002': {'description': 'Mello Yellow',
                                      'product_type':'Soda',
                                      'quantity_available': 10},
                          })

    def test_show_rentals_works(self):
        """
        Test that we can retrieve customers who have rented a given product.
        """
        products = [
            {'product_id': 'p0', 'description': 'Gum',
             'product_type': 'Candy', 'quantity_available': '5'},
            {'product_id': 'p1', 'description': 'Atomic Fireball',
             'product_type': 'Candy', 'quantity_available': '0'},
        ]
        db.DATABASE['product'].insert_many(products)

        customers = [
            {'customer_id': 'c0', 'first_name': 'Mickey',
             'last_name': 'Mouse', 'address': '123 4th Ave',
             'phone': 1234567890, 'email': 'mickey@any.com'},
            {'customer_id': 'c1', 'first_name': 'Minnie',
             'last_name': 'Mouse', 'address': '234 5th Ave',
             'phone': 2345678901, 'email': 'minnie@any.com'},
            {'customer_id': 'c2', 'first_name': 'Donald',
             'last_name': 'Duck', 'address': '345 6th Ave',
             'phone': 3456789012, 'email': 'donald@any.com'}
        ]
        db.DATABASE['customer'].insert_many(customers)

        rentals = [
            {'rental_id': 'r0', 'customer_id': 'c0', 'product_id': 'p0'},
            {'rental_id': 'r1', 'customer_id': 'c2', 'product_id': 'p0'},
            {'rental_id': 'r2', 'customer_id': 'c1', 'product_id': 'p1'},
            {'rental_id': 'r3', 'customer_id': 'c2', 'product_id': 'p1'}
        ]
        db.DATABASE['rental'].insert_many(rentals)

        p0_renters = db.show_rentals('p0')
        self.assertEqual(p0_renters,
                         {'c0': {'name': 'Mickey Mouse',
                                 'address': '123 4th Ave',
                                 'phone_number': 1234567890,
                                 'email': 'mickey@any.com'},
                          'c2': {'name': 'Donald Duck',
                                 'address': '345 6th Ave',
                                 'phone_number': 3456789012,
                                 'email': 'donald@any.com'},
                          })

        p1_renters = db.show_rentals('p1')
        self.assertEqual(p1_renters,
                         {'c1': {'name': 'Minnie Mouse',
                                 'address': '234 5th Ave',
                                 'phone_number': 2345678901,
                                 'email': 'minnie@any.com'},
                          'c2': {'name': 'Donald Duck',
                                 'address': '345 6th Ave',
                                 'phone_number': 3456789012,
                                 'email': 'donald@any.com'},
                          })
