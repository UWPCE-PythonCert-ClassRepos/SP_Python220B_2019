"""Launches the user interface for the inventory management system"""
import sys
import market_prices
import inventory_class
import furniture_class
import electric_appliances_class


class MainInventoryManagement:
    """
    A class-based system for inventory management
    """
    def __init__(self):
        self.full_inventory = {}

    def main_menu(self, user_prompt=None):
        """Prints a prompt for menu options and calls the action chosen by the user"""
        valid_prompts = {"1": self.add_new_item,
                         "2": self.item_info,
                         "q": self.exit_program}
        options = list(valid_prompts.keys())

        while user_prompt not in valid_prompts:
            options_str = ("{}" + ", {}" * (len(options)-1)).format(*options)
            print(f"Please choose from the following options ({options_str}):")
            print("1. Add a new item to the inventory")
            print("2. Get item information")
            print("q. Quit")
            user_prompt = input(">")
        return valid_prompts.get(user_prompt)

    @staticmethod
    def get_price(item_code):
        """Gets the price from market_prices based on a provided item_code"""
        price = market_prices.get_latest_price(item_code)
        return price

    def add_new_item(self):
        """
        Prompts for item_code, item_description, and item_rental_price from the user.
        Gets the item price from market_prices based off item_code.
        Asks questions to find out what type of item it is and asks for more inputs based
        on the type of item, then adds the item to full_inventory.
        """
        item_code = input("Enter item code: ")
        item_description = input("Enter item description: ")
        item_rental_price = input("Enter item rental price: ")

        # Get price from the market prices module
        item_price = market_prices.get_latest_price(item_code)

        is_furniture = input("Is this item a piece of furniture? (Y/N): ")
        if is_furniture.lower() == "y":
            item_material = input("Enter item material: ")
            item_size = input("Enter item size (S,M,L,XL): ")
            new_item = furniture_class.Furniture(item_code, item_description, item_price,
                                                 item_rental_price, item_material, item_size)
        else:
            is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
            if is_electric_appliance.lower() == "y":
                item_brand = input("Enter item brand: ")
                item_voltage = input("Enter item voltage: ")
                new_item = electric_appliances_class.ElectricAppliances(
                    item_code, item_description, item_price, item_rental_price,
                    item_brand, item_voltage)
            else:
                new_item = inventory_class.Inventory(
                    item_code, item_description, item_price, item_rental_price)
        self.full_inventory[item_code] = new_item.return_as_dictionary()
        print("New inventory item added")

    def item_info(self):
        """
        Asks for item_code and if the item is in the full_inventory prints the item info.
        If the item isn't found prints a message.
        """
        item_code = input("Enter item code: ")
        if item_code in self.full_inventory:
            print_dict = self.full_inventory[item_code]
            for k, v in print_dict.items():
                print("{}:{}".format(k, v))
        else:
            print("Item not found in inventory")

    @staticmethod
    def exit_program():
        """Exits the program"""
        sys.exit()


if __name__ == '__main__':
    MAIN_PROGRAM = MainInventoryManagement()
    while True:
        print(MAIN_PROGRAM.full_inventory)
        MAIN_PROGRAM.main_menu()
        input("Press Enter to continue...........")
