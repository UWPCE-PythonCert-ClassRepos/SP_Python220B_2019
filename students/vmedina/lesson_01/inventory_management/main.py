""" Launches the user interface for the inventory management system"""
import sys
import inventory_management.market_prices as market_prices
import inventory_management.inventory_class as inventory
import inventory_management.furniture_class as furniture
import inventory_management.electric_appliances_class as electricappliances

FULL_INVENTORY = {}


def main_menu(user_prompt=None):
    """
    :param user_prompt:
    :type user_prompt:
    :return:
    :rtype:
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print("Please choose from the following options({}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    """
    :param item_code:
    :type item_code:
    :return:
    :rtype:
    """
    price = market_prices.get_latest_price(item_code)
    return price


def add_new_item():
    """
    :return:
    :rtype:
    """
    global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    itemprice = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture.Furniture(item_code, item_description, itemprice,
                                       item_rental_price, item_material, item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electricappliances.ElectricAppliances(item_code, item_description,
                                                             itemprice, item_rental_price,
                                                             item_brand, item_voltage)
        else:
            new_item = inventory.Inventory(item_code, item_description, itemprice,
                                           item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    :return:
    :rtype:
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")


def inventory_specs():
    """

    :return:
    """
    return FULL_INVENTORY


def exit_program():
    """

    :return:
    :rtype:
    """
    sys.exit()


if __name__ == '__main__':

    while True:
        main_menu()()
        input("Press Enter to continue...........")
