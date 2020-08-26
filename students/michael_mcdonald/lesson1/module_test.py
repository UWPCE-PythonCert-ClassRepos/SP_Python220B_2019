from unittest import TestCase
from lesson1.inventory_management import electric_appliances_class as eac

SAMPLE_ELEC_ITEM_DICT = {10: {'product_code': 10, 'description': 'Blender', 'market_price': 24,
                              'rental_price': 24, 'brand': 'Omega', 'voltage': '120'}}
"""test eac return as dictionary"""

# integration testing
# linting
# for each set of tests create a class
# cd C:\Users\mimcdona\Dropbox\UW\UW-Python220_Project
# python -m unittest lesson1\test_unit.py
# python -m coverage run --source=inventory_management -m unittest test_unit.py
# python -m coverage report



class TestElectricAppliances(TestCase):
    """test ElectricAppliances class"""

    def test_return_as_dictionary(self):
        """test eac return as dictionary"""

        sample_dict = list(SAMPLE_ELEC_ITEM_DICT.values())[0]
        lst = list(sample_dict.values())
        new_eac_item = eac.ElectricAppliances(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])
        test_dict = new_eac_item.return_as_dictionary()
        self.assertEqual(test_dict, sample_dict)
    print('- TestElectricAppliances.test_return_as_dictionary complete -')
