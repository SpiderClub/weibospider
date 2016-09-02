# 获取转发信息# -*-coding:utf-8 -*-
from multiprocessing import Process, Manager
from get_cookie import get_session
from task.get_repost import get_all
from time import sleep


def time_task():
    sleep(22*60*60)


if __name__ == '__main__':
    while True:
        mgr = Manager()
        d = mgr.dict()
        pw = Process(target=get_session, args=(d,))
        pr = Process(target=get_all, args=(d,))
        pw.start()
        # 防止pr先执行
        sleep(60)
        pr.start()
        pr.join()
        pw.terminate()
        print('本轮抓取已经结束')
        sleep(60*60*2)



