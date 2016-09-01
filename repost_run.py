# 获取转发信息# -*-coding:utf-8 -*-
from multiprocessing import Process, Queue
from get_cookie import get_session
from task.get_repost import get_all
from time import sleep


def time_task():
    sleep(22*60*60)


if __name__ == '__main__':
    while True:
        q = Queue()
        pw = Process(target=get_session, args=(q,))
        pr = Process(target=get_all, args=(q,))
        pt = Process(target=time_task)
        pw.start()
        pr.start()
        pt.start()
        # 等待pt结束(pt作为定时器)
        pt.join()
        # 强制结束pw
        pr.terminate()
        pw.terminate()
        print('本轮抓取已经结束')
        sleep(60*60*2)



