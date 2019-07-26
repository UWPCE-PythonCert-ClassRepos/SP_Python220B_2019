import sys
import threading
import time
from queue import Queue

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




# #class thread
# class MyThread(threading.Thread):

#     def run(self):
#         print("hello from %s" % threading.current_thread().name)

# thread = MyThread()
# thread.start()



# # thread locking and releasing with a function, used for accessing same data to protect data integrity
# # eg. one thread accessing first half of data and second thread accessing second half and then both of them writing new data

# lock = threading.Lock()

# def f():
#     lock.acquire()
#     print("%s got lock" % threading.current_thread().name)
#     time.sleep(1)
#     lock.release()
#     print("%s got released" % threading.current_thread().name)

# threading.Thread(target=f).start()
# threading.Thread(target=f).start()
# threading.Thread(target=f).start()


# #using aquire
# lock = threading.Lock()
# lock.acquire()
# if not lock.acquire(False):
#     print("couldn't get lock")
# lock.release()
# if lock.acquire(False):
#     print("got lock")



# q = Queue(maxsize=10)
# q.put(37337)
# block = True
# timeout = 2
# print(q.get(block, timeout))



# timed events
# def called_once():
#     """
#     this function is designed to be called once in the future
#     """
#     print("I just got called! It's now: {}".format(time.asctime()))

# # setting it up to be called
# t = threading.Timer(interval=3, function=called_once)
# t.start()

# you can cancel it if you want:
# t.cancel()


