
"""
This module defines the whole workflow of the application.
"""

# Launches the user interface for the inventory management system
import sys
from .market_prices import get_latest_price
from .inventory_class import Inventory
from .furniture_class import Furniture
from .electric_appliances_class import ElectricAppliances

FULL_INVENTORY = {}


def main_menu(user_prompt=None):
    """
    Show main menu.
    :param user_prompt: User input
    :return: corresponding action
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}

    while user_prompt not in valid_prompts:
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(price=24):
    """
    Print "Get price"
    :return:
    """
    print("Get price")
    return get_latest_price(price)


def add_new_item():
    """
    Add an item to inventory
    :return: None
    """
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_latest_price()

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = Furniture(item_code, item_description, item_price,
                             item_rental_price,
                             item_material, item_size)
    else:
        is_electric_appliance = input(
            "Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = ElectricAppliances(item_code, item_description,
                                          item_price,
                                          item_rental_price,
                                          item_brand, item_voltage)
        else:
            new_item = Inventory(item_code, item_description, item_price,
                                 item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    Print item's metadata.
    :return: Dict or None
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for k, val in print_dict.items():
            print("{}:{}".format(k, val))
    else:
        print("Item not found in inventory")
    return FULL_INVENTORY.get(item_code)


def exit_program():
    """
    Exit the program
    :return: None
    """
    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
