# 获取转发信息# -*-coding:utf-8 -*-
from multiprocessing import Process, Queue
from get_cookie import get_session
from task.get_repost import get_all
from time import sleep


if __name__ == '__main__':
    while True:
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
        sleep(60*60*2)



