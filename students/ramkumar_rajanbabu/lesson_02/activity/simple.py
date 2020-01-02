# simple.py

import logging

# Change to level to logging.WARNING from logging.DEBUG
log_format= "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
#logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')

# BEGIN NEW STUFF
# Create a "formatter" using our format string
formatter = logging.Formatter(log_format)

# Create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.WARNING)
# Set the formatter for this log message handler to the formatter we created above.
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Get the "root" logger.
logger = logging.getLogger()
# Add our file_handler to the "root" logger's handlers.
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# END NEW STUFF

def my_fun(n):
    for i in range(0, n):
        logging.debug(i) #replaces print statement
        if i ==50:
            logging.warning("The value of i is 50.")
        try:    
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)