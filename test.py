from multiprocessing import Process, Manager
from time import sleep
from gl import headers
from get_cookie import get_session
from do_dataget.basic import get_page

urls = [
        'http://weibo.com/1692900573/E83Sb3wNL?refer_flag=1001030103_ ',
        'http://weibo.com/2132294577/E82LWdbRH?refer_flag=1001030103_ ',
        'http://weibo.com/p/1005055204394362/info?mod=pedit_more',
        'http://weibo.com/p/1005052906744981/info?mod=pedit_more'
        ]


def test_url(dic, url_list):
    session = dic['session']
    for url in url_list:
        get_page(url, session, headers)


if __name__ == '__main__':
    mgr = Manager()
    d = mgr.dict()
    pw = Process(target=get_session, args=(d,))
    pr = Process(target=test_url, args=(d, urls))

    pw.start()
    sleep(30)
    pr.start()
    pr.join()
    pw.terminate()
    pw.join()