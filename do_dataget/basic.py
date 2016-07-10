import time, sys, logging, gl, requests
from gl import time_out, login_name
from do_dataprocess.basic import is_403, is_404


def get_page(session, url, headers, user_verify=True):
    """
    :param session:
    :param url:
    :param headers:
    :param user_verify: 验证是否是抓取用户或者微博信息，否为抓取转发的ajax连接
    :return:
    """
    print('本次抓取的url为{url}'.format(url=url))
    try:
        page = session.get(url, headers=headers, timeout=time_out, verify=False, stream=False).text.\
            encode('utf-8',  'ignore').decode('utf-8')
        gl.count += 1
        time.sleep(40)
        if user_verify:
            if is_403(page):
                logging.info('账号{username}已经被冻结'.format(username=login_name))
                logging.info('它的页面源码为{page}'.format(page=page))
                logging.info('本次抓取结束，时间是:{curtime}，一共抓取了{count}个页面'.format(curtime=time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime()), count=gl.count))
                sys.exit(-1)
            if is_404(page):
                print('url为{url}的连接不存在'.format(url=url))
                logging.info('url为{url}的连接不存在'.format(url=url))
                logging.info('它的页面源码为{page}'.format(page=page))
                return ''
    except TimeoutError:
        print('抓取{url}超时'.format(url=url))
        return ''
    except requests.exceptions.ConnectionError:
        logging.info('新浪服务器拒绝连接，程序休眠5分钟')
        time.sleep(60*5) # 休眠5分钟
    else:
        return page
