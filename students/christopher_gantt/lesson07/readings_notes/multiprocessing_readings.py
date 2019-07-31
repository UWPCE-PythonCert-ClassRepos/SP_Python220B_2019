import multiprocessing
from multiprocessing import Pipe, Pool
import os
import time

# def func():
#     print("hello from process %s" % os.getpid())
#     time.sleep(1)

# proc = multiprocessing.Process(target=func, args=())
# proc.start()
# proc = multiprocessing.Process(target=func, args=())
# proc.start()



# parent_conn, child_conn = Pipe()
# child_conn.send("foo")
# print(parent_conn.recv())


def f(x):
    return x*x
if __name__ == '__main__':
    pool = Pool(processes=4)

    result = pool.apply_async(f, (10,))
    print(result.get(timeout=1))
    print(pool.map(f, range(10)))

    it = pool.imap(f, range(10))
    print(it.next())
    print(it.next())
    print(it.next(timeout=1))

    # result = pool.apply_async(time.sleep, (10,))
    # print(result.get(timeout=1))