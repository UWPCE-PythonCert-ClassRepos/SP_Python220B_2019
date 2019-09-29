'''
Context manager for Ballard Locks
'''

class Locke:
    '''
    Create instance of Locke context manager with specified capacity
    '''
    def __init__(self, capacity):
        print('__init__({})'.format(capacity))
        self.capacity = capacity

    '''
    Called when 'with' is used, returns context manager
    '''
    def __enter__(self):
        print('__enter__({:d})'.format(self.capacity))
        return self

    '''
    Method to move boats through locke
    '''
    def move_boats_through(self, boats):
        print('Attempting to move {:d} boats through'.format(boats))
        if boats > self.capacity:
            raise Exception('Too many boats!')

    '''
    Called when context manager is finished
    '''
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_val}')
            print(f'exc_traceback: {exc_tb}')
            print('exception handled')
        return True

if __name__ == '__main__':
    '''
    Test context manager by creating small and large lockes, then try to move
    boats through such that the large locke doesn't have enough capacity but the
    large locke does
    '''
    # Create lockes
    small_locke = Locke(5)
    large_locke = Locke(10)
    # Define number of boats to move through
    boats = 8
    # Attempt to move through large locke
    with large_locke as locke:
        print('Inside CM (large)')
        locke.move_boats_through(boats)
    # Attempt to move through small locke
    with small_locke as locke:
        print('Inside CM (small)')
        locke.move_boats_through(boats)
    # If we do not handle the exception in the __exit__ method, the code
    # below will never be called. This may or may not be desired.
    print('Code execution continues...')
