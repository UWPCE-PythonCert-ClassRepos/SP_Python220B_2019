"""
Test cases for inventory.py
"""

import unittest
import os
import inventory

_dir = os.path.dirname(os.path.realpath(__file__))
TEST_ITEMS = os.path.join(_dir, "test_items.csv")
TEST_CSV = os.path.join(_dir, "test_all.csv")


class TestInventory(unittest.TestCase):
    """Test inventory functions"""

    @classmethod
    def setUpClass(cls) -> None:
        """Remove TEST_CSV"""
        try:
            os.remove(TEST_CSV)
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove TEST_CSV"""
        os.remove(TEST_CSV)

    def setUp(self) -> None:
        pass

    def test_add_furniture(self):
        """Tests inventory.add_furniture"""
        try:
            with open(TEST_CSV) as f:
                lines_pre = f.readlines()
        except FileNotFoundError:
            lines_pre = []

        # Add single furniture item
        inventory.add_furniture(TEST_CSV, "Elisa Miles", "LR04", "Leather Sofa", 25)

        with open(TEST_CSV) as f:
            lines = f.readlines()
        new_lines = lines[len(lines_pre):]
        self.assertEqual(1, len(new_lines))
        self.assertEqual("Elisa Miles,LR04,Leather Sofa,25.00", new_lines[0].strip())

        # Add another item
        inventory.add_furniture(TEST_CSV, "Edward Data", "KT78", "Kitchen Table", 10)

        with open(TEST_CSV) as f:
            lines = f.readlines()
        new_lines = lines[len(lines_pre):]
        self.assertEqual(2, len(new_lines))
        self.assertEqual("Elisa Miles,LR04,Leather Sofa,25.00", new_lines[0].strip())
        self.assertEqual("Edward Data,KT78,Kitchen Table,10.00", new_lines[1].strip())

        # Remove file and assert that it will be created
        os.remove(TEST_CSV)
        inventory.add_furniture(TEST_CSV, "Edward Data", "KT78", "Kitchen Table", 10)
        with open(TEST_CSV) as f:
            lines = f.readlines()
        self.assertEqual(1, len(lines))
        self.assertEqual("Edward Data,KT78,Kitchen Table,10.00", lines[0].strip())

    def test_single_customer(self):
        """Tests inventory.single_customer"""

        try:
            with open(TEST_CSV) as f:
                lines_pre = f.readlines()
        except FileNotFoundError:
            lines_pre = []

        create_invoice = inventory.single_customer("Susan Wong", TEST_CSV)
        create_invoice(TEST_ITEMS)

        with open(TEST_CSV) as f:
            lines = f.readlines()

        new_lines = lines[len(lines_pre):]
        self.assertEqual(3, len(new_lines))
        self.assertEqual("Susan Wong,LR04,Leather Sofa,25.00", new_lines[0].strip())
        self.assertEqual("Susan Wong,KT78,Kitchen Table,10.00", new_lines[1].strip())
        self.assertEqual("Susan Wong,BR02,Queen Mattress,17.00", new_lines[2].strip())
