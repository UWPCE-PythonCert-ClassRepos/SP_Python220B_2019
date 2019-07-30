'''activity.py'''

class Context:
    """
    From Doug Hellmann, PyMOTW
    https://pymotw.com/3/contextlib/#module-contextlib
    """

    def __init__(self, handle_error):
        print('__init__({})'.format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        return self.handle_error

class Locke:
    '''ballard locks problem'''
    def __init__(self, num):
        print('__init__({})'.format(num))
        self.num = num

    def __enter__(self):
        print('__enter__()')
        return self

    def move_boats_thorugh(self, boats):
        print(boats)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        # return self.handle_error


if __name__ == '__main__':
    # with Locke(5):
    #     print('this is in the context')

    small_locke = Locke(5)
    boats = 8
    with small_locke as locke:
        locke.move_boats_thorugh(boats)

    # with Context(True) as foo:
    #     print('This is in the context')
    #     raise RuntimeError('this is the error message')


