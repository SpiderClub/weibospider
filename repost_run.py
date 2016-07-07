# 获取转发信息# -*-coding:utf-8 -*-
import time
from multiprocessing import Process, Queue
from get_cookie import get_session
from task.get_repost import get_all


if __name__ == '__main__':
    while True:
        # 父进程创建Queue并传递给各个子进程
        q = Queue()
        pw = Process(target=get_session, args=(q,))
        pr = Process(target=get_all, args=(q,))
        pw.start()
        pr.start()
        # 等待pr结束
        pr.join()
        # 强制结束pw
        pw.terminate()
        print('本轮抓取已经结束')
        time.sleep(2*60*60)




