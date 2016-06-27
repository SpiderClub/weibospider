# -*-coding:utf-8 -*-
import time
import logging
import gl
from do_login import login_info
from task.get_repost import get_reposts
from db_operation import weibosearch_dao


# todo 用装饰器设置定时功能
if __name__ == '__main__':

    while True:
        session = login_info.get_session()
        urls = weibosearch_dao.get_crawl_urls()
        logging.info('本次抓取时间为:{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        print('共需要{num}条微博'.format(num=len(urls)))
        print('----------------------------------')
        for url in urls:
            print('当前取得url为{url}'.format(url=url))
            get_reposts(url, session, gl.headers)
            print('-------------------------------------------')
            time.sleep(60)
        print('本次抓取结束,结束时间为{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        time.sleep(60*60*1)

