import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"  # Add/modify these

# Create a "formatter" using our format string
formatter = logging.Formatter(log_format)

# Create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)           
console_handler.setFormatter(formatter)

# Get the "root" logger. More on that below.
logger = logging.getLogger()
# Need to specify level for root logger since default is WARNING
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)



# simple.py
def my_fun(n):
    for i in range(0, n):
        if i == 50:
            logging.warning("Value of i is 50")
        try: 
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}".format(i))

if __name__ == "__main__":
    my_fun(100)