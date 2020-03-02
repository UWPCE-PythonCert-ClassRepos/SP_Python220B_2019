# Advanced Programming in Python -- Lesson 7 Assignment 1
# Jason Virtue
# Start Date 2/23/2020

#Original code set with multiple threads writing to stdout and text gets scrambled
import random
import sys
import threading
import time

#No locks to prevent race condition. STDOUT Function. Sleep condition causing unequal function durations
def write():
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")

#Run function 50 times with a fixed sleep timeframe
for i in range(50):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    time.sleep(.1)
