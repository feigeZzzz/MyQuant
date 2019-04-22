# encoding:utf-8
from multiprocessing import Process
import os, time, random


# 线程启动后实际执行的代码块
def r1(process_name):
    for i in range(5):
        print(process_name, os.getpid())  # 打印出当前进程的id
        time.sleep(random.random())


def r2(process_name):
    for i in range(5):
        print(process_name, os.getpid())  # 打印出当前进程的id
        time.sleep(random.random() * 2)


if __name__ == "__main__":
    print("main process run...")
    p1 = Process(target=r1, args=('process_name1',))  # target:指定进程执行的函数，args:该函数的参数，需要使用tuple
    p2 = Process(target=r2, args=('process_name2',))

    p1.start()  # 通过调用start方法启动进程，跟线程差不多。
    p2.start()  # 但run方法在哪呢？待会说。。。
    #p1.join()  # join方法也很有意思，寻思了一下午，终于理解了。待会演示。
    #p2.join()
    print("main process runned all lines...")