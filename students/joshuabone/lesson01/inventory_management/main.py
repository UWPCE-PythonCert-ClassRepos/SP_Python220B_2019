"""Launches the user interface for the inventory management system"""
import sys
import inventory_management.market_prices as market_prices
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


class MainMenu:
    """User interface for the inventory management system"""
    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else dict()
        self.valid_prompts = {"1": self.add_new_item,
                              "2": self.item_info,
                              "q": self.exit_program}

    def main_menu(self, user_prompt=None):
        """Main Menu"""

        options = list(self.valid_prompts.keys())

        while user_prompt not in self.valid_prompts:
            options_str = ("{}" + ", {}" * (len(options) - 1)).format(*options)
            print(f"Please choose from the following options ({options_str}):")
            print("1. Add a new item to the inventory")
            print("2. Get item information")
            print("q. Quit")
            user_prompt = input(">")
        return self.valid_prompts.get(user_prompt)

    def add_new_item(self):
        """Add New Item"""
        item_code = input("Enter item code: ")
        item_description = input("Enter item description: ")
        item_rental_price = input("Enter item rental price: ")

        # Get price from the market prices module
        item_price = market_prices.get_latest_price(item_code)

        is_furniture = input("Is this item a piece of furniture? (Y/N): ")
        if is_furniture.lower() == "y":
            item_material = input("Enter item material: ")
            item_size = input("Enter item size (S,M,L,XL): ")
            new_item = Furniture(item_code, item_description, item_price,
                                 item_rental_price, item_material, item_size)
        else:
            is_electric_appliance = input(
                "Is this item an electric appliance? (Y/N): ")
            if is_electric_appliance.lower() == "y":
                item_brand = input("Enter item brand: ")
                item_voltage = input("Enter item voltage: ")
                new_item = ElectricAppliances(item_code, item_description,
                                              item_price, item_rental_price,
                                              item_brand, item_voltage)
            else:
                new_item = Inventory(item_code,
                                     item_description,
                                     item_price,
                                     item_rental_price)
        self.inventory[item_code] = new_item.return_as_dictionary()
        print("New inventory item added")

    def item_info(self):
        """Item Info"""
        item_code = input("Enter item code: ")
        if item_code in self.inventory:
            print_dict = self.inventory[item_code]
            for k, val in print_dict.items():
                print("{}:{}".format(k, val))
        else:
            print("Item not found in inventory")

    def do_menu(self, loop=True):
        """Do the main menu loop"""
        print(self.inventory)
        self.main_menu()()
        input("Press Enter to continue...........")
        if loop:
            self.do_menu()

    @staticmethod
    def get_price():
        """Get Price"""
        print("Get price")

    @staticmethod
    def exit_program():
        """Exit Program"""
        sys.exit()


if __name__ == '__main__':
    MainMenu().do_menu()
