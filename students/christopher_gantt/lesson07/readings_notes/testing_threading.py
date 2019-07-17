'''testing_threading.py'''
import time
import threading


def func1(statement):
    for i in range(5):
        print("hello from thread %s" % statement)
        time.sleep(1)

func1('thread one')
func1('thread two')
func1('thread three')




#simple thread
def func():
    for i in range(5):
        print("hello from thread %s" % threading.current_thread().name)
        time.sleep(1)

threads = []
for i in range(3):
    thread = threading.Thread(target=func, args=())
    thread.start()
    threads.append(thread)


# next step for implementing, do three separate importing functions

# figure out how to time it when it when the thread finishes, try timeit.timeit(function)
