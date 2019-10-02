# Note that main.iten_info has already been tested extensively in test_unit.py.

import sys
import inventory_management.market_prices as mp
from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliance import ElectricAppliance


FULL_INVENTORY = {}


def main_menu(user_prompt=None):
    """ Present user with menu, gather user input, and return the appropriate
    function name.

    Keyword arguments:
        user_prompt
    """

    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        # Pylint is flagging options_str as an unused variable yet it is being used on the next
        # line.
        # pylint: disable=unused-variable
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = get_user_input(">")
    return valid_prompts.get(user_prompt)


# Never called so commented out.
# def get_price(item_price):
#     print("Get price")

def add_new_item():
    """ Collect information to add an inventory item and create it.
    """
    # global fullInventory  # uhm - let's avoid globals, ok?

    item_code, item_description, item_rental_price, item_price = collect_product_info()

    if get_is_furniture().lower() == "y":

        item_material, item_size = collect_furniture_info()

        new_item = Furniture(product_code=item_code,
                             description=item_description,
                             rental_price=item_rental_price,
                             market_price=item_price,
                             material=item_material,
                             size=item_size)
    elif get_is_electric_appliance().lower() == "y":

        item_brand, item_voltage = collect_electric_appliance_info()

        new_item = ElectricAppliance(product_code=item_code,
                                     description=item_description,
                                     rental_price=item_rental_price,
                                     market_price=item_price,
                                     brand=item_brand,
                                     voltage=item_voltage)
    else:
        new_item = Inventory(product_code=item_code,
                             description=item_description,
                             rental_price=item_rental_price,
                             market_price=item_price)

    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")
    return FULL_INVENTORY[item_code]


def collect_product_info():
    """ Collect common info for Inventory items.
    """
    item_code = get_item_code()
    item_description = get_item_description()
    item_rental_price = get_item_rental_price()

    # Get price from the market prices module
    item_price = mp.get_latest_price(item_code)

    return item_code, item_description, item_rental_price, item_price


def collect_furniture_info():
    """ Collect info for Furniture-type items.
    """
    item_material = get_item_material()
    item_size = get_item_size()

    return item_material, item_size


def collect_electric_appliance_info():
    """ Collect info for ElectricAppliance-type items.
    """
    item_brand = get_item_brand()
    item_voltage = get_item_voltage()

    return item_brand, item_voltage


def get_item_code():
    """ Invoke UI to get item code.
    """
    return get_user_input("Enter item code: ")


def get_item_description():
    """ Invoke UI to get item description.
    """
    return get_user_input("Enter item description: ")


def get_item_rental_price():
    """ Invoke UI to get item rental price.
    """
    return get_user_input("Enter item rental price: ")


def get_is_furniture():
    """ Invoke UI to get whether or not the item is furniture.
    """
    return get_user_input("Is this item a piece of furniture? (Y/N): ")


def get_item_material():
    """ Invoke UI to get item material.
    """
    return get_user_input("Enter item material: ")


def get_item_size():
    """ Invoke UI to get item size.
    """
    return get_user_input("Enter item size (S,M,L,XL): ")


def get_is_electric_appliance():
    """ Invoke UI to get whether or not the item is an electric appliance.
    """
    return get_user_input("Is this item an electric appliance? (Y/N): ")


def get_item_brand():
    """ Invoke UI to get item brand.
    """
    return get_user_input("Enter item brand: ")


def get_item_voltage():
    """ Invoke UI to get item voltage.
    """
    return get_user_input("Enter item voltage: ")


def get_user_input(message):
    """ Collect user input.

    Keyword arguments
        message - test to include for the user prompt.
    """
    return input(message)


def item_info():
    """ Output an inventory item's attributes and attribute values to stdout. Also return it from
    the function.
    """
    info = ""
    all_info = []
    item_code = get_item_code()
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for item_attribute, attribute_value in print_dict.items():
            info = "{}:{}".format(item_attribute, attribute_value)
            print(info)
            all_info.append(info)
        return all_info

    info = "Item not found in inventory"
    print(info)
    return info


def exit_program():
    """ Exit the program.
    """
    return sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        get_user_input("Press Enter to continue...........")
