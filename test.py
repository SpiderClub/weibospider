from multiprocessing import Process, Manager
from time import sleep
from gl import headers
from get_cookie import get_session
from do_dataget.basic import get_page

urls = [
        'http://weibo.com/1876859923/E7P06wBPF',
        'http://weibo.com/p/1005051892723783/info?mod=pedit_more',
        'http://weibo.com/5547774767/E8P8tDE7S?refer_flag=1001030103_ ',
        'http://weibo.com/1959451603/E8ON3qbgN?refer_flag=1001030103_ ',
        'http://weibo.com/1489996535/E8qWY7DvF ',
        'http://weibo.com/5256023028/E8rOylASJ?refer_flag=1001030103_ '
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