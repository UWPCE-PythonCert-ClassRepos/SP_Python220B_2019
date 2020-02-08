class Locke(object):
    """ Context manager simulation of a marine lock.
    """
    def __init__(self, max_boats):
        self._max_boats = max_boats
        self._num_requested = 0  # We don't know how many boats will try to enter the lock yet

    @property
    def max_boats(self):
        return self._max_boats

    @property
    def num_requested(self):
        return self._num_requested

    @num_requested.setter
    def num_requested(self, value):
        self._num_requested = value
        if value > self._max_boats:
            raise ValueError('The number of boats that requested to enter exceeded the maximum.')
            

    def __enter__(self):
        print("In __enter__")
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("In __exit__")
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        if exc_type == ValueError:
            print(exc_val)
            print("{} were allowed to enter the lock, {} were not.".format(self.max_boats,
                                                                           self.num_requested - self.max_boats))
        return True

    def move_boats_through(self, num_requested):
        print("In move_boats_through")
        self.num_requested = num_requested

        
if __name__ == '__main__':
    # small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
