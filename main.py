# -*-coding:utf-8 -*-
import time
import logging
import gl
from do_login import login_info
from task.get_userinfo import get_users_info


# todo 用装饰器设置定时功能
if __name__ == '__main__':

    while True:
        session = login_info.get_session()
        get_users_info(session, gl.headers)
        logging.info('本次抓取时间为:{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))

        print('本次抓取结束,结束时间为{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        logging.info('本次抓取结束，时间是:{curtime}，一共抓取了{count}个页面'.format(curtime=time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime()), count=gl.count))
        time.sleep(2*60*60)



