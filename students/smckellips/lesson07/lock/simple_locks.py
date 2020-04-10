import threading
import time
import datetime

lock = threading.Lock()

def f():
    lock.acquire()
    print("%s got lock" % threading.current_thread().name)
    time.sleep(1)
    lock.release()

start = datetime.datetime.now()

threading.Thread(target=f).start()
threading.Thread(target=f).start()
threading.Thread(target=f).start()

end = datetime.datetime.now()

print(end - start)