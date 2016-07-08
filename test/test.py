from multiprocessing import Process, Queue
import os, time, random
import logging


# 写数据进程执行的代码:
def write(que):
    log_path = os.path.join(os.getcwd(), 'write.log')
    logging.basicConfig(filename=log_path, level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y%m%d %H:%M:%S')
    while True:
        logging.info('Process to write: %s' % os.getpid())
        que.put(random.randint(0, 10))
        time.sleep(2)


# 读数据进程执行的代码:
def read(que):
    log_path = os.path.join(os.getcwd(), 'read.log')
    logging.basicConfig(filename=log_path, level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y%m%d %H:%M:%S')
    print('Process to read: %s' % os.getpid())
    value = que.get(True)
    logging.info('Get %s from queue.' % value)
    time.sleep(10)


if __name__ == '__main__':
    path = os.getcwd()
    parent_path = os.path.dirname(path)
    print(parent_path)
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

