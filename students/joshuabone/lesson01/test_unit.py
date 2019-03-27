"""Unit Tests for Inventory Management"""
import unittest

from inventory_management.electric_appliances_class import ElectricAppliances


class ElectricalApplianceTests(unittest.TestCase):
    """Unit Tests for Electrical Appliance"""
    def test_electric_appliance_todict(self):
        """Test that electrical appliance returns as dictionary"""
        fields = ("productCode", "description", "marketPrice", "rentalPrice",
                  "brand", "voltage")
        app = ElectricAppliances(*fields)
        expected = {f: f for f in fields}
        self.assertEqual(app.return_as_dictionary(), expected)
