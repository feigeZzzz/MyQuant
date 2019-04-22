#!/usr/bin/env.python
import threading, time
lock = threading.Lock()
lock.acquire()
lock.release()
count = 0
class Mythread(threading.Thread):
    def __init__(self, threadName):
        super().__init__(name=threadName)
        self.lock = lock

    def run(self):
        global count
        self.lock.acquire()
        for i in range(100):
            count += 1
            time.sleep(0.1)
            print(self.getName(), count)
        self.lock.release()

if __name__ == '__main__':
    for i in range(2):
        Mythread('MythreadName:' + str(i)).start()