import logging

logging.basicConfig(level=logging.WARNING)
def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        100 / (50 - i)

if __name__ == "__main__":
    my_fun(100)