import unittest
import create_db
import customer_model as cm
import basic_operations as bo

class BasicOpsTests(unittest.TestCase):

    def setUp(self):
        create_db.main()

    def tearDown(self):
        try:
            cm.Identity.drop_table()
            cm.Contact.drop_table()

        except Exception as e:
            print(f"Exception occurred: {e}")
        cm.database.close()

    def test_check_tables(self):
        assert cm.Identity.table_exists()
        assert cm.Contact.table_exists()

    def test_add(self):
        # Add customers to the table
        bo.add_customer('12345', 'Max', 'Tucker', '412 23rd ave SW', '505-519-2432', 'tuckmax@gmail.com', True, 45600)
        bo.add_customer('432', 'Dude', 'Abides', '801 NE 108th', '206-519-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('525', 'Lindsey', 'Back', '525 N. 39th Way', '480-832-1442', 'lback@gmail.com', True, 45600)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', True, 1200)

        # Ensure that there's 4 records total
        user_count = cm.Identity.select().count()
        self.assertEqual(4, user_count)

    def test_delete(self):
        # Add customers to the table
        bo.add_customer('12345', 'Max', 'Tucker', '412 23rd ave SW', '505-519-2432', 'tuckmax@gmail.com', True, 45600)
        bo.add_customer('432', 'Dude', 'Abides', '801 NE 108th', '206-519-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('525', 'Lindsey', 'Back', '525 N. 39th Way', '480-832-1442', 'lback@gmail.com', True, 45600)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', True, 1200)

        # Test delete
        bo.delete_customer('12345')
        bo.delete_customer('525')
        user_count = cm.Identity.select().count()
        user_not_found1 = cm.Identity.select().where(cm.Identity.customer_id == '525')
        user_not_found2 = cm.Identity.select().where(cm.Identity.customer_id == '12345')
        self.assertEqual(None, user_not_found1)
        self.assertEqual(None, user_not_found2)
        self.assertEqual(2, user_count)

        # Delete rest of users
        bo.delete_customer('5612')
        bo.delete_customer('432')
        user_count = cm.Identity.select().count()
        self.assertEqual(0, user_count)

    def test_search(self):
        bo.add_customer('789', 'Baxter', 'Dog', '2300 43rd ave SW', '506-219-2522', 'bdog@gmail.com', True, 500)
        bo.add_customer('12', 'Frank', 'Abigail', '400 8th St.', '400-555-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('700', 'Devon', 'Hamlin', '589 28 Alpine Dr', '302-818-2415', 'dham@gmail.com', True, 1200)

        # Store customer information into dictionaries
        customer1 = bo.search_customer('7894')
        customer2 = bo.search_customer('789')
        customer3 = bo.search_customer('700')

        customer2_dict = {
            'name': 'Baxter',
            'lastname': 'Dog',
            'email_address': 'bdog@gmail.com',
            'phone_number': '506-219-2522'
        }
        customer3_dict = {
            'name': 'Devon',
            'lastname': 'Hamlin',
            'email_address': 'dham@gmail.com',
            'phone_number': '302-818-2415'
        }


        self.assertEqual({}, customer1)
        self.assertEqual(customer2_dict, customer2)
        self.assertEqual(customer3_dict, customer3)

    def test_update_credit(self):
        with self.assertRaises(ValueError):
            bo.update_customer_credit('2342', 1300)

        # Add customers
        bo.add_customer('12345', 'Max', 'Tucker', '412 23rd ave SW', '505-519-2432', 'tuckmax@gmail.com', True, 45600)
        bo.add_customer('432', 'Dude', 'Abides', '801 NE 108th', '206-519-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('525', 'Lindsey', 'Back', '525 N. 39th Way', '480-832-1442', 'lback@gmail.com', True, 45600)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', True, 1200)

        # Ensure ValueError exception is raised
        with self.assertRaises(ValueError):
            bo.update_customer_credit('2342', 1300)
            bo.update_customer_credit('500', 1300)
            bo.update_customer_credit('169', 1300)

        # Update customer credit
        bo.update_customer_credit('432', 7000)
        bo.update_customer_credit('5612', 1300)

        # Verify that customer creidt was updated
        credit_query1 = cm.Identity.select(cm.Identity.credit_limit).where(cm.Identity =='432')
        credit_query2 = cm.Identity.select(cm.Identity.credit_limit).where(cm.Identity == '5612')
        self.assertEqual(7000, credit_query1)
        self.assertEqual(1300, credit_query2)

    def test_active_customers(self):
        # Test before adding customers
        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(bo.list_active_customers(), active_count)

        bo.add_customer('12345', 'Max', 'Tucker', '412 23rd ave SW', '505-519-2432', 'tuckmax@gmail.com', True, 45600)
        bo.add_customer('432', 'Dude', 'Abides', '801 NE 108th', '206-519-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', True, 1200)

        # Test active count function
        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(bo.list_active_customers(), active_count)

        # Add more customers and rerun the test
        bo.add_customer('525', 'Lindsey', 'Back', '525 N. 39th Way', '480-832-1442', 'lback@gmail.com', True, 45600)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', False, 1200)

        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(bo.list_active_customers(), active_count)


class IntegrationsTest(unittest.TestCase):
    def setUp(self):
        create_db.main()

        self.customer1_dict = {
            'name': 'Baxter',
            'lastname': 'Dog',
            'email_address': 'bdog@gmail.com',
            'phone_number': '506-219-2522'
        }
        self.customer2_dict = {
            'name': 'Devon',
            'lastname': 'Hamlin',
            'email_address': 'dham@gmail.com',
            'phone_number': '302-818-2415'
        }

    def tearDown(self):
        try:
            cm.Identity.drop_table()
            cm.Contact.drop_table()

        except Exception as e:
            print(f"Exception occurred: {e}")

        cm.database.close()

    def test_functions(self):
        # Run tests before making changes to database
        with self.assertRaises(ValueError):
            bo.update_customer_credit('400', 1300)
            bo.delete_customer('5612')

        customer_init = bo.search_customer('7894')
        self.assertEqual({}, customer_init)

        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(bo.list_active_customers(), active_count)

        # Add all customers
        bo.add_customer('12345', 'Max', 'Tucker', '412 23rd ave SW', '505-519-2432', 'tuckmax@gmail.com', True, 45600)
        bo.add_customer('432', 'Dude', 'Abides', '801 NE 108th', '206-519-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('525', 'Lindsey', 'Back', '525 N. 39th Way', '480-832-1442', 'lback@gmail.com', True, 45600)
        bo.add_customer('5612', 'Brian', 'Newton', '250 Camus Dr', '602-432-2313', 'bnewton@gmail.com', True, 1200)
        bo.add_customer('789', 'Baxter', 'Dog', '2300 43rd ave SW', '506-219-2522', 'bdog@gmail.com', True, 500)
        bo.add_customer('12', 'Frank', 'Abigail', '400 8th St.', '400-555-4032', 'biglebowski@gmail.com', False, 300)
        bo.add_customer('700', 'Devon', 'Hamlin', '589 28 Alpine Dr', '302-818-2415', 'dham@gmail.com', True, 1200)

        user_count = cm.Identity.select().count()
        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(7, user_count)
        self.assertEqual(bo.list_active_customers(), active_count)


        customer1 = bo.search_customer('789')
        customer2 = bo.search_customer('700')
        self.assertEqual(self.customer1_dict, customer1)
        self.assertEqual(self.customer2_dict, customer2)

        # Test that ValueError gets raised for invalid customer IDs.
        with self.assertRaises(ValueError):
            bo.update_customer_credit('712', 1300)
            bo.delete_customer('512')
            bo.update_customer_credit('2342', 1300)

        bo.update_customer_credit('432', 25000)
        credit_query1 = cm.Identity.select(cm.Identity.credit_limit).where(cm.Identity == '432')
        self.assertEqual(25000, credit_query1)

        # Delete users from database
        bo.delete_customer('12')
        bo.delete_customer('789')

        # Ensure correct records were deleted and nothing more
        user_count_delete = cm.Identity.select().count()
        user_not_found1 = cm.Identity.select().where(cm.Identity.customer_id == '12')
        user_not_found2 = cm.Identity.select().where(cm.Identity.customer_id == '789')
        self.assertEqual(5, user_count_delete)
        self.assertEqual(None, user_not_found1)
        self.assertEqual(None, user_not_found2)

        # Ensure active count integrity is intact
        active_count = cm.Identity.select().where(cm.Identity.active == True).count()
        self.assertEqual(bo.list_active_customers(), active_count)

        customer_post = bo.search_customer('789')
        self.assertEqual({}, customer_post)

        with self.assertRaises(ValueError):
            bo.update_customer_credit('712', 1300)
            bo.delete_customer('512')

        # Test updating customer credit
        bo.update_customer_credit('5612', 46987)
        credit_query = cm.Identity.select(cm.Identity.credit_limit).where(cm.Identity == '432')
        self.assertEqual(46987, credit_query)


if __name__ == '__main__':
    unittest.main()