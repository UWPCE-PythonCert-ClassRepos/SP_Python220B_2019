import unittest
import customer_model as cm

class IdentityTables(unittest.TestCase):

    def setUp(self):
        cm.database.create_tables(cm.Identity, safe=True)

    def tearDown(self):
        try:
            cm.database.drop_tables(cm.Identity)
        except:
            pass
        cm.database.close()

    def test_check(self):
        assert cm.Identity.table_exists()


    def test_checker(self):
        with self.assertRaises(cm.OperationalError):
            cm.database.create_tables(cm.Identity)


    def test_drop_table(self):
        cm.database.drop_tables(cm.Identity)
        assert cm.Identity.table_exists() == False


"""class UserTableTests(unittest.TestCase):


    def setUp(self):
        cm.DATABASE.connect()
        try:
            cm.DATABASE.create_table(cm.User)
        except:
            pass
        cm.User.create(
                username='testUsername',
                email='testEmail@testEmail.com')
        cm.DATABASE.close()

    def tearDown(self):
        cm.User.delete().where(cm.User.username=='testUsername').execute()

    def test_create_username(self):
        user = cm.User.get(username='testUsername')
        self.assertEqual(user.username, 'testUsername')

    def test_safe(self):
        with self.assertRaises(cm.IntegrityError):
            cm.User.create(
                username='testUsername',
                email='testEmail@testEmail.com')"""



if __name__ == '__main__':
    unittest.main()