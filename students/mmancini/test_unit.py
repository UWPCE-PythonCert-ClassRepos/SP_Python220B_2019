#!/usr/bin/env python3

"""
Unit Testing Inventory Management
"""

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import inventory_management.main as main


class MainTests(TestCase):
    """ test main """

    def setUp(self):
        """ setup """
		
		
    def test_main_menu(self):
        """Test that the user inputs"""

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

