from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from ..inventory_management.furniture import Furniture
from ..inventory_management.inventory import Inventory
from ..inventory_management.electric_appliances import ElectricAppliances
from ..inventory_management.market_prices import get_latest_price as MP

class FurnitureTests(TestCase):

    def setUp(self):
        self.new_chair = Furniture(1321, 'Chair', 1203.05, 35.00, 'wood', 'XL')

    def test_create_furniture(self):
        
        self.assertEqual(self.new_chair.size, 'XL')
        self.assertEqual(self.new_chair.material, 'wood')
        self.assertEqual(self.new_chair.rental_price, 35.00)
        self.assertEqual(self.new_chair.market_price, 1203.05)
        self.assertEqual(self.new_chair.description, 'Chair')
        self.assertEqual(self.new_chair.product_code, 1321)

    
    def test_return_as_dict(self):
        self.assertEqual(self.new_chair.return_as_dictionary().get('product_code'), 1321)
        self.assertEqual(self.new_chair.return_as_dictionary().get('description'), 'Chair')
        self.assertEqual(self.new_chair.return_as_dictionary().get('market_price'), 1203.05)
        self.assertEqual(self.new_chair.return_as_dictionary().get('rental_price'), 35.00)
        self.assertEqual(self.new_chair.return_as_dictionary().get('material'), 'wood')
        self.assertEqual(self.new_chair.return_as_dictionary().get('size'), 'XL')

class InventoryTests(TestCase):

    def setUp(self):
        pass



    def test_inventory_creation(self):
        pass


class ElectricAppliancesTests(TestCase):
    
    def setUp(self):
        self.microwave = ElectricAppliances(1573, 'Samsung Microwave', 120.00, 125.00, 'Samsung', 120)


    def test_create_appliance(self):
        self.assertEqual(self.microwave.product_code, 1573)
        self.assertEqual(self.microwave.description, 'Samsung Microwave')
        self.assertEqual(self.microwave.market_price, 120.00)
        self.assertEqual(self.microwave.rental_price, 125.00)
        self.assertEqual(self.microwave.brand, 'Samsung')
        self.assertEqual(self.microwave.voltage, 120)


    def test_appliance_dict(self):
        self.assertEqual(self.microwave.return_as_dictionary().get('product_code'), 1573)
        self.assertEqual(self.microwave.return_as_dictionary().get('description'), 'Samsung Microwave')
        self.assertEqual(self.microwave.return_as_dictionary().get('market_price'), 120.00)
        self.assertEqual(self.microwave.return_as_dictionary().get('rental_price'), 125.00)
        self.assertEqual(self.microwave.return_as_dictionary().get('brand'), 'Samsung')
        self.assertEqual(self.microwave.return_as_dictionary().get('voltage'), 120)
    

class MarketPricesTests(TestCase):


    def setUp(self):
        self.tv_code = 24332
        self.table_code = 89773
        self.lamp_code = 7346

        self.tv = ElectricAppliances(self.tv_code, 'Samsung TV', 1200.00, 125.00, 'Samsung', 120)
        self.table = Furniture(self.table_code, 'Coffee Table', 300.00, 125.00, 'Glass', 'L')
        self.lamp = ElectricAppliances(self.lamp_code, 'Bed side lamp', 20.00, 23.00, 'Target', 9)

    def test_market_price(self):
        market_price = MP(self.lamp.product_code)

        self.assertEqual(market_price, 24)


    def test_tv_market_price(self):
        MP.get_latest_price = Mock(return_value=456)
        price = MP.get_latest_price(self.tv.product_code)

        self.assertEqual(price, 456)


    def test_table_market_price(self):
        MP.get_latest_price = Mock(return_value=self.table.market_price)
        table_price = MP.get_latest_price(self.table_code)

        self.assertEqual(table_price, self.table.market_price)


"""class MainTests(TestCase):

    def test_main_menu(self):
        menu_select = '1'
        expected = 'add_new_item'
        with patch('builtins.input', side_effect=menu_select):
            self.assertEqual(Mock.patch.get_user_input(), expected)"""