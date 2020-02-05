# Advanced Programming In Python - Lesson 7 Activity 1: Threading & Concurrency
# RedMine Issue - SchoolOps-17
# Code Poet: Anthony McKeever
# Start Date: 01/07/2019
# End Date: 01/07/2019

import random
import sys
import threading
import time

# Locking object to help prevent thread race conditions on resources.
lock = threading.Lock()

def write():
    # Lock the lock object to stop race conditions on sys.stdout and allow the
    # method to complete inside thread.
    lock.acquire()

    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")

    # Unlock the lock object to allow othre threads to lock it, otherwise the
    # other threads will need to wait until the current thread has joined the
    # main thread.
    lock.release()

thread_list = []
for i in range(100):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    thread_list.append(thread)
    time.sleep(.1)

# Join the threads in the list back into the main thread so the application
# will wait until all work is complete before exiting.
for thread in thread_list:
    thread.join()
