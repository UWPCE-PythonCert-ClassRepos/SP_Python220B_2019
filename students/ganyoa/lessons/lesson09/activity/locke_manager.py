"""
Advanced Programming in Python Lesson 9
Activity: Ballard Locks
"""

class Locke:

    def __init__(self, max):
        """Initialize the Locke class"""
        self.pump_on = True
        self.door_open = False
        self.max = max

    def __enter__(self):
        """stops the pumps and opens the door the entry"""
        print("Stopping the pumps.")
        self.pump_on = False
        print("Opening the doors.")
        self.door_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the doors and restarts the pumps"""
        print("Closing the doors.")
        self.door_open = False
        print("Restarting the pumps.")
        self.pump_on = True

    def move_boats_through(self, boats):
        """determine if the number of boats can transit"""
        if boats > self.max:
            msg = f"The locke can only support {self.max} boats."
            raise ValueError(msg)

        print(f"{boats} will transit the lockes")

        for i in range(boats):
            print(f"Boat #{i + 1} entered the locke")

        print(f"{boats} boats transitted the lockes")

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    # with small_locke as locke:
    #     locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    # with large_locke as locke:
    #     locke.move_boats_through(boats)