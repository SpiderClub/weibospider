# 获取转发信息# -*-coding:utf-8 -*-
from multiprocessing import Process, Manager
from time import sleep, ctime
from get_cookie import get_session
from task.get_repost import get_all
from utils.util_mtd import display_count


if __name__ == '__main__':
    while True:
        mgr = Manager()
        d = mgr.dict()
        pw = Process(target=get_session, args=(d,))
        pw.daemon = True
        pr = Process(target=get_all, args=(d,))
        print('本轮抓取开始,开始时间为{endtime}'.format(endtime=ctime()))

        pw.start()
        # 防止pr先执行
        sleep(90)
        pr.start()
        pr.join()

        pw.terminate()
        print('本轮抓取已经结束,结束时间为{endtime}'.format(endtime=ctime()))
        pw.join() # 使其可以更新状态

        sleep(60*60)



