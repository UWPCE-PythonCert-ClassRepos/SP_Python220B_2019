from unittest import TestCase
from unittest.mock import MagicMock, patch

import inventory_management.market_prices as market_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main


class ModuleTests(TestCase):

    def test_module(self):
        # testing option 1: add_new_item().
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')

        main.get_latest_price = MagicMock()
        main.get_latest_price.return_value = 24
        electric_appliance_inputs = ['001', 'oven', 12, 'n', 'y',
                                     'GE', 120]
        with patch('builtins.input', side_effect=electric_appliance_inputs):
            main.add_new_item()
            self.assertEqual(len(main.FULL_INVENTORY), 1)
            self.assertEqual(main.FULL_INVENTORY[0].product_code, '001')
            self.assertEqual(main.FULL_INVENTORY[0].description, 'oven')
            self.assertEqual(main.FULL_INVENTORY[0].market_price, 24)
            self.assertEqual(main.FULL_INVENTORY[0].rental_price, 12)
            self.assertEqual(main.FULL_INVENTORY[0].brand, 'GE')
            self.assertEqual(main.FULL_INVENTORY[0].voltage, 120)

        # testing option 2: item_info().
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')
            with patch('builtins.input', side_effect=['001']):
                with patch('builtins.print') as fakeoutput:
                    main.item_info() # print the information of item 001
                    fakeoutput.assert_called_with(main.FULL_INVENTORY[0])

        # testing option 3: exit_program().
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')
        with self.assertRaises(SystemExit) as texit:
            main.exit_program()
            the_exception = texit.exception
            self.assertEqual(the_exception.code, 3)
