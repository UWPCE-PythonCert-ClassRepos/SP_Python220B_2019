"""
contains get_latest_price module
"""

# pylint: disable=R0801
# pylint: disable=R0903
# pylint:disable=duplicate-code

def get_latest_price(item_code):
    """
    :param item_code:
    :type item_code:
    :return:
    :rtype:
    """
    if isinstance(item_code, int):
        return 24
    return 24
    # Raise an exception to force the user to Mock its output
