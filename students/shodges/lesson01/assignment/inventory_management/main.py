"""
Launches the user interface for the inventory management system
"""
import sys
from inventory_management import inventory_class
from inventory_management import furniture_class
from inventory_management import market_prices
from inventory_management import electric_appliances_class

INVENTORY_DATA = {}

def main_menu(user_prompt=None):
    """
    Standard function to prompt the user with a menu and wait for input.
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def add_new_item():
    """
    Function to add an item (with user input) to the FULL_INVENTORY
    """
    item_code = input("Enter item code: ")
    INVENTORY_DATA['item_code'] = item_code
    INVENTORY_DATA['description'] = input("Enter item description: ")
    INVENTORY_DATA['market_price'] = market_prices.get_latest_price(item_code)
    INVENTORY_DATA['rental_price'] = input("Enter item rental price: ")

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        INVENTORY_DATA['material'] = input("Enter item material: ")
        INVENTORY_DATA['size'] = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(**INVENTORY_DATA)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            INVENTORY_DATA['brand'] = input("Enter item brand: ")
            INVENTORY_DATA['voltage'] = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(**INVENTORY_DATA)
        else:
            new_item = inventory_class.Inventory(**INVENTORY_DATA)
    INVENTORY_DATA[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")

def get_price(item_code):
    """
    Function to retrieve the price given item_code
    """
    return "Current price of {}: {}".format(item_code, market_prices.get_latest_price(item_code))


def item_info():
    """
    Function to retrieve the item (specified with user input) details from FULL_INVENTORY.
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for item_key, item_value in print_dict.items():
            print("{}:{}".format(item_key, item_value))
    else:
        print("Item not found in inventory")

def exit_program():
    """
    Callback from menu to exit.
    """
    sys.exit()

if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
