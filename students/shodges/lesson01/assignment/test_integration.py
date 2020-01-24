from unittest import TestCase
from unittest.mock import patch
import sys

sys.path.append('inventory_management')

import main

class IntegrationTest(TestCase):
    """Integration test cases"""
    def test_integration(self):
        """Test the integrated application"""
        with patch('builtins.input', side_effect=['1', '64', 'Nintendo 64', '5.64', 'n', 'n']):
            main.add_new_item()
