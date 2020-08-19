"""test inventory management integration"""
import unittest
from unittest import TestCase
from unittest.mock import patch
import lesson1.inventory_management.main as ma  # pylint: disable=import-error
from lesson1.test_unit import SAMPLE_GENE_ITEM_DICT  # pylint: disable=import-error
from lesson1.test_unit import SAMPLE_ELEC_ITEM_DICT  # pylint: disable=import-error
from lesson1.test_unit import SAMPLE_FURN_ITEM_DICT  # pylint: disable=import-error


class TestIntegration(TestCase):
    """test inventory management integration"""
    ma.FULL_INVENTORY = {}
    sample_valid_prompts = ['1', '2', 'q']
    current_valid_prompt_cnt = 3

    # pylint: disable-msg=too-many-locals
    def test_inventory_management(self):
        """test inventory management integration"""

        counter = 0
        input_chair = [100, 'Chair', 24, 'y', 'wood', 'L']
        input_blender = [10, 'Blender', 24, 'n', 'y', 'Omega', '120']
        input_tape = [1, 'Tape', 24, 'n', 'n']

        # input
        for i in TestIntegration.sample_valid_prompts:
            with patch('builtins.input', side_effect=i):
                if i == 1:
                    self.assertEqual(ma.main_menu(), ma.add_new_item)
                if i == 2:
                    self.assertEqual(ma.main_menu(), ma.item_info)
                if i == 'q':
                    self.assertEqual(ma.main_menu(), ma.exit_program)
            counter = counter + 1
        self.assertEqual(TestIntegration.current_valid_prompt_cnt, counter)

        # add_new_item
        with patch('builtins.input', side_effect=input_chair):
            new_furn_item = ma.add_new_item()
        with patch('builtins.input', side_effect=input_blender):
            new_eac_item = ma.add_new_item()
        with patch('builtins.input', side_effect=input_tape):
            new_generic_item = ma.add_new_item()
        print(new_furn_item)
        print(new_eac_item)
        print(new_generic_item)
        self.assertEqual(3, len(ma.FULL_INVENTORY))
        self.assertEqual(SAMPLE_GENE_ITEM_DICT[1], ma.FULL_INVENTORY[1])  # tape
        self.assertEqual(list(SAMPLE_ELEC_ITEM_DICT.values())[0], ma.FULL_INVENTORY[10])  # blender
        self.assertEqual(list(SAMPLE_FURN_ITEM_DICT.values())[0], ma.FULL_INVENTORY[100])  # chair

        # item_info
        generic_info_print = 'product_code: 1\ndescription: ' \
                             'Tape\nmarket_price: 24\nrental_price: 24\n'
        item_code = [1]
        with patch('builtins.input', side_effect=item_code):
            tape_info = ma.item_info()
        self.assertEqual(print(generic_info_print), print(tape_info))

        elec_info_print = 'product_code: 10\ndescription:Blender\nmarket_price:' \
                          '24\nrental_price:24\nbrand:Omega\nvoltage:120\n'
        item_code = [10]
        with patch('builtins.input', side_effect=item_code):
            blender_info = ma.item_info()
            print(blender_info)
        self.assertEqual(print(elec_info_print), print(blender_info))
        furn_info_print = 'product_code: 100\ndescription:Chair\nmarket_price:' \
                          '24\nrental_price:24\nmaterial:wood\nsize:L\n'
        item_code = [100]
        with patch('builtins.input', side_effect=item_code):
            chair_info = ma.item_info()
            print(blender_info)
        self.assertEqual(print(furn_info_print), print(chair_info))

if __name__ == "__main__":
    unittest.main()
