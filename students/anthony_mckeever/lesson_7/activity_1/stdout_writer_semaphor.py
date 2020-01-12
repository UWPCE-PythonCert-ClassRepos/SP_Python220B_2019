# Advanced Programming In Python - Lesson 7 Activity 1: Threading & Concurrency
# RedMine Issue - SchoolOps-17
# Code Poet: Anthony McKeever
# Start Date: 01/07/2019
# End Date: 01/07/2019

import random
import sys
import threading
import time

# Semaphore object to help throttle resource dependencies.
semaphore = threading.Semaphore(2)

def write():
    # Lock the semaphore object to throttle the number of calls to the
    # sys.stdout.write method.  Note some threads might print over others as
    # the semaphore allows multiple threads to aquire it simultaneously.
    semaphore.acquire()

    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")

    # Release the semaphore object to allow other threads to access it.  If not
    # released other threads will only be able to acquire it once the current
    # thread has joined main.
    semaphore.release()

thread_list = []
for i in range(100):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    thread_list.append(thread)
    time.sleep(.1)

# Join the threads back to the main thread.
# In this case we have some fun with pop!
while thread_list:
    thread = thread_list.pop()
    thread.join()
