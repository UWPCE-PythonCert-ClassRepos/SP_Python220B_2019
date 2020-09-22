"""
Advanced Programming in Python Lesson 9
Activity: Ballard Locks with decorator
"""
from contextlib import contextmanager

@contextmanager
def locke(max_boats):

    try:
        print("Stopping the pumps.")
        pump_on = False
        print("Opening the doors.")
        door_open = True

        yield

    except Exception as e:
        print('error occured within yielded resource')
        raise e

    finally:
        print("Closing the doors.")
        door_open = False
        print("Restarting the pumps.")
        pump_on = True


if __name__ == '__main__':
    boats = 7
    max_boats = 9
    locke_capacity = locke(max_boats)


    def move_boats_through(boats):
        if boats > max_boats:
            msg = f"Lockes can support {max_boats} boats, {boats} scheduled."
            raise ValueError(msg)
        print(f"{boats} will pass through the lockes")

        for i in range(boats):
            print(f"Boat #{i + 1} entered the locke")

        print(f"{boats} boats passed the lockes")
        return move_boats_through


    with locke_capacity:
        move_boats_through(boats)