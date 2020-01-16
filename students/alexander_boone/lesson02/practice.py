#!/usr/bin/env python
import logging

# Create a format string to be used by a formatter
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
# Create a formatter using the above format string
formatter = logging.Formatter(log_format)

# Create a log message handler that sends the output to 'mylog.log'
file_handler = logging.FileHandler('mylog.log')
# Set file handler level to debug at a level of warning or above
file_handler.setLevel(logging.WARNING)
# Set the formatter for this log message handler to the formatter we created above
file_handler.setFormatter(formatter)

# Similarly, create console handler for output to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
console_handler.setFormatter(formatter)  

# Get the 'root' logger
logger = logging.getLogger()
# Set level to DEBUG (warning is default for the 'root' logger)
logger.setLevel(logging.DEBUG)
# Add our file handler to the 'root' logger's handlers
logger.addHandler(file_handler)
# Add our console handler to the 'root' logger's handlers
logger.addHandler(console_handler)

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)