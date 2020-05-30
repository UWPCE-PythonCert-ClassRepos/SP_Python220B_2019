"""Unit Testing the Inventory Management script"""

import sys
sys.path.append('./inventory_management')
from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
from inventory_management.market_prices import get_latest_price

