from unittest import TestCase
from unittest.mock import patch
import patch_tutorial as pt

class TestPatchTutorial(TestCase):

    # Patch gets list of responses
    def test_get_user_input_human(self):
        # Have to use patch for multiple responses
        responses = ('Luis', 'Conejo', '40', 'n')
        expected = 'You are Luis Conejo, age 40'

        with patch('builtins.input',side_effect=responses):
            self.assertEqual(pt.get_user_input(), expected)