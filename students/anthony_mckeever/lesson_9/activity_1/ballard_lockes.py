# Advanced Programming In Python - Lesson 9 Activity 1: Context Managers
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 01/22/2019
# End Date: 01/22/2019

"""
A module for managing the Ballard Lockes
"""


class Locke():
    """
    A class representing a locke.
    """

    def __init__(self, max_boats):
        """
        Initializes a Locke class.

        :max_boats:     The maximum number of boats the locke can support.
        """
        self.pumps_armed = True
        self.doors_open = False
        self.max_boats = max_boats

    def __enter__(self):
        """
        Primes the lock by stoping the pumps and opening the doors
        """
        print("Stopping pumps...")
        self.pumps_armed = False
        print("Opening doors...")
        self.doors_open = True
        print("Locke ready for boat transit.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the doors and reengages the pumps
        """
        print("Closing doors...")
        self.doors_open = False
        print("Starting pumps...")
        self.pumps_armed = True
        print("Locke is now closed.")

    def move_boats_through(self, boat_count):
        """
        Allows boats to transit through the locke.

        :boat_count:    The number of boats that are in transit.
        """
        if boat_count > self.max_boats:
            msg = f"The current locke can only support {self.max_boats} boats."
            raise ValueError(msg)

        if self.pumps_armed or not self.doors_open:
            msg = str("The locke has not been primed for through traffic.  "
                      + "Try wrapping the locke object in a \"with\" statement"
                      + " to properly engage the locke.")
            raise RuntimeError(msg)

        print(f"Moving {boat_count} through the locke...")

        for i in range(boat_count):
            print(f"Boat #{i + 1}: toot toot!")

        print("Boat transit complete.")
