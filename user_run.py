# 获取指定用户的信息
# -*-coding:utf-8 -*-
import time
from multiprocessing import Process, Queue
from get_cookie import get_session
from task.get_userinfo import get_users_info


if __name__ == '__main__':
    while True:
        q = Queue()
        pw = Process(target=get_session, args=(q,))
        pr = Process(target=get_users_info, args=(q,))
        pw.start()
        pr.start()
        # 等待pr结束
        pr.join()
        # 强制结束pw
        pw.terminate()
        print('本轮抓取结束')
        time.sleep(2*60*60)