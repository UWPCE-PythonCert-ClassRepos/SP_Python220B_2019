# Stella Kim
# Activity 9: Advanced Language Constructs

"""Software control system for the Ballard Locks"""


class Locke():
    """Lock context manager"""
    def __init__(self, capacity):
        print('__init__({})'.format(capacity))
        self.capacity = capacity

    def __enter__(self):
        print('__enter__({})'.format(self.capacity))
        print('Stopping the pumps.')
        return self

    def move_boats_through(self, boats):
        """Checks the number of boats passing through lock"""
        if boats > self.capacity:
            raise Exception('Closing the doors.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        print('Restarting the pumps.')
        return self


if __name__ == '__main__':
    SMALL_LOCKE = Locke(5)
    LARGE_LOCKE = Locke(10)
    BOATS = 8

    # Too many boats through a small locke will raise an exception
    with SMALL_LOCKE as locke:
        print('Opening the doors.')
        locke.move_boats_through(BOATS)

    # A lock with sufficient capacity can move boats without incident.
    with LARGE_LOCKE as locke:
        print('Opening the doors.')
        locke.move_boats_through(BOATS)
