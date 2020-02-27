# Advanced Programming in Python -- Lesson 7 Assignment 1
# Jason Virtue
# Start Date 2/23/2020

#Original code set with multiple threads writing to stdout and with locks to prevent race condition
import random
import sys
import threading
import time

#Lock condition to lock each thread till it completes
lock = threading.Lock()

#Locks to prevent race condition. STDOUT Function. Sleep condition causing unequal function durations
def write():
    lock.acquire()
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")
    lock.release()

#Run function 50 times with a fixed sleep timeframe
threads = []
for i in range(50):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    threads.append(thread)
    time.sleep(.01)

# Now join() them all so the program won't terminate early
# required because these are all daemon threads
for thread in threads:
    thread.join()

