"""Script for managing locks, but poorly"""

from time import sleep

class Lock():
    """base functions for all locks"""

    def __init__(self, boats, capacity):
        self.boats = boats
        self.capacity = capacity
        self.pumps_on = False
        self.doors_open = False

    def stop_the_pumps(self):
        """Shuts off the pumps"""
        self.pumps_on = False

    def start_the_pumps(self):
        """Shuts off the pumps"""
        self.pumps_on = True

    def close_the_door(self):
        """closes the doors to the lock"""
        self.doors_open = False

    def open_the_door(self):
        """closes the doors to the lock"""
        self.doors_open = True

    def __enter__(self):
        """attempts to move boats throught the locks"""
        while self.boats > 0:
            if self.pumps_on:
                self.stop_the_pumps()
            if not self.doors_open:
                self.open_the_door()
            print("Waiting for ships to enter")
            sleep(1)
            self.close_the_door()
            self.start_the_pumps()
            print("Waiting for locks to fill")
            sleep(1)
            self.stop_the_pumps()
            self.open_the_door()
            print("Waiting for ships to leave")
            sleep(1)
            self.boats = max(self.boats - self.capacity, 0)
            print('{} boats left to move throguh'.format(self.boats))
        return self.boats

    def __exit__(self, *args):
        print("All boats are through")


if __name__ == '__main__':
    with Lock(15, 10) as big_lock:
        pass

    with Lock(15, 5) as small_lock:
        pass
