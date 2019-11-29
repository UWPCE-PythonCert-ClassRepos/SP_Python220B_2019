from unittest import TestCase
from unittest.mock import Mock, patch
import mock_tutorial as mt 

class TutorialTests(TestCase):
    def test_get_user_info(self):
        # We are hi-jacking input, not the name variable
        mt.input = Mock(return_value = 'Luis')
        self.assertEqual(mt.get_user_info(), 'Luis')

    def test_get_current_temperature_nice(self):
        mt.temperature_sensor.read_temperature = Mock(return_value = 75)
        expected_response = 'Nice temperature, 75'
        self.assertEqual(mt.get_current_temp(),expected_response)

    def test_get_current_temperature_below_zero(self):
        mt.temperature_sensor.read_temperature = Mock(return_value = =10)
        self.assertRaises(OverFlowError, mt.get_current_temp())    