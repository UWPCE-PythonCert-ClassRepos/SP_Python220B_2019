import queue
from threading import Thread

def foo():
    print('hello')
    return 'foo'

que = queue.Queue()

t = Thread(target=lambda q: q.put(foo()), args=(que,))
t.start()
t.join()
result = que.get()
print(result)



# import Queue
# from threading import Thread

# def foo(bar):
#     print('hello {0}'.format(bar))
#     return 'foo'

# que = Queue.Queue()

# t = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
# t.start()
# t.join()
# result = que.get()
# print(result)




# import Queue
# from threading import Thread

# def foo(bar):
#     print('hello {0}'.format(bar))
#     return 'foo'

# que = Queue.Queue()
# threads_list = list()

# t = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
# t.start()
# threads_list.append(t)

# # # Add more threads here
# # ...
# # threads_list.append(t2)
# # ...
# # threads_list.append(t3)
# # ...

# # Join all the threads
# for t in threads_list:
#     t.join()

# # Check thread's return value
# while not que.empty():
#     result = que.get()
#     print(result)
