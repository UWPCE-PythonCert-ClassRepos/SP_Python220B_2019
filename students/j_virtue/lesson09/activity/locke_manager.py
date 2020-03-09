'''Module to control lock system'''
# Advanced Programming in Python -- Lesson 9 Activity 1
# Jason Virtue
# Start Date 3/01/2020

class Locke:
    '''Class to open and close locke'''
   
    def __init__(self, capacity):
        '''Initialize the locke class'''
        self.run_pump = True
        self.open_door = False
        self.capacity = capacity

    def __enter__(self):
        '''Open doors to locks for boats to enter'''
        print("Stopping the pumps.")
        self.run_pump = False
        print("Opening the doors.")
        self.open_door = True
        print("Doors open and boats can enter")
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        '''Closes the doors and starts pumps'''
        print("Closing the doors.")
        self.open_door = False
        print("Restarting the pumps.")
        self.run_pump = True
    
    def move_boats_through(self, boats):
        '''Boat allowed to enter lock'''
        if boats > self.capacity:
            msg = f"Lock can only support {self.capacity} boats."
            raise ValueError(msg)

        print(f"{boats} boats will enter the lock...")

        for i in range(boats):
            print(f"Boat #{i + 1}: enters!")

        print("Boat transit complete.")

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Small locke lots of boats
    #with small_locke as locke:
    #    locke.move_boats_through(boats)

    # Right size locke for number of boats
    with large_locke as locke:
        locke.move_boats_through(boats)
    

