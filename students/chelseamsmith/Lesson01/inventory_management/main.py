"""Launches the user interface for the inventory management system"""
import sys
import inventory_management.market_prices as market_prices
import inventory_management.inventory_class as inventory_class
import inventory_management.furniture_class as furniture_class
import inventory_management.electric_appliances_class as electric_appliances_class
FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """prompts user to choose from a menu until a valid option is chosen,
    then returns name of a function corresponding to choice"""
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


def get_price(code):
    """gets price from market prices module"""
    price = market_prices.get_latest_price(code)
    return price


def add_new_item():
    """gets information about a new item from user,
    then enters item into inventory"""
    code = input("Enter item code: ")
    description = input("Enter item description: ")
    rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    price = market_prices.get_latest_price(code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        material = input("Enter item material: ")
        size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(code, description, price,
                                             rental_price, material, size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            brand = input("Enter item brand: ")
            voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(code, description, price,
                                                                    rental_price, brand, voltage)
        else:
            new_item = inventory_class.Inventory(code, description, price,
                                                 rental_price)
    FULL_INVENTORY[code] = new_item.return_as_dictionary()
    print("New inventory item added")

def return_inventory():
    """returns inventory"""
    return FULL_INVENTORY

def item_info():
    """gets an item code from user, checks if a code in the inventory,
    then prints item details if it is or prints item not found if it isn't"""
    code = input("Enter item code: ")
    if code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[code]
        for k, val in print_dict.items():
            print("{}:{}".format(k, val))
    else:
        print("Item not found in inventory")

def exit_program():
    """exits the program"""
    sys.exit()

if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
