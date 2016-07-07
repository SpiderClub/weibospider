from multiprocessing import Process, Queue
import os, time, random


# 写数据进程执行的代码:
def write(que):
    while True:
        print('Process to write: %s' % os.getpid())
        que.put(random.randint(0, 10))
        time.sleep(2)


# 读数据进程执行的代码:
def read(que):
    print('Process to read: %s' % os.getpid())
    value = que.get(True)
    print('Get %s from queue.' % value)
    time.sleep(10)


if __name__ == '__main__':
    while True:
        # 父进程创建Queue，并传给各个子进程：
        q = Queue()
        pw = Process(target=write, args=(q,))
        pr = Process(target=read, args=(q,))
        # 启动子进程pw，写入:
        pw.start()
        # 启动子进程pr，读取:
        pr.start()
        # 等待pr结束
        pr.join()
        # 使pw强制结束
        pw.terminate()
        print('现在pw已经结束，开始睡眠5秒')
        time.sleep(5)

