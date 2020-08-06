"""
test_integration.py
by David Baylor

integration tests the inventory_manegment module.
"""

from unittest import TestCase
from unittest.mock import MagicMock

import inventory_management.__main__ as main

class IntegrationTest(TestCase):
    """integration test for inventory_management"""
    def test_integration(self):
        """adds a Book, Chair, and Computer to the inventory and then views them bofore exiting"""

        main.input = MagicMock()
        main.input.side_effect = ["1", "1234", "Book", "$10", "N", "N", "",
                                  "1", "1111", "Chair", "$25", "Y", "Wood", "S", "",
                                  "1", "2222", "Computer", "$100", "N", "Y", "Dell", "120", "",
                                  "2", "1111", "",
                                  "2", "2222", "",
                                  "q"]
        with self.assertRaises(SystemExit):
            main.run()
