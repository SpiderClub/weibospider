import time
import requests
from logger.log import crawler
from page_parse.basic import is_403, is_404, is_complete
from decorator.decorators import timeout_decorator, timeout
from config.get_config import get_timeout, get_crawl_interal, get_excp_interal


time_out = get_timeout()
interal = get_crawl_interal()
excp_interal = get_excp_interal()


@timeout(200)
@timeout_decorator
def get_page(url, session, headers, user_verify=True):
    """
    :param user_verify: 是否为可能出现验证码的页面(搜索页面的403还没解析)，否为抓取转发的ajax连接
    """
    crawler.info('本次抓取的url为{url}'.format(url=url))
    try:
        page = session.get(url, headers=headers, timeout=time_out, verify=False).text. \
            encode('utf-8', 'ignore').decode('utf-8')
        time.sleep(interal)

        if user_verify:
            if is_403(page):
                crawler.warning('本账号已经被冻结')
                crawler.warning('它的页面源码为{page}'.format(page=page))
                crawler.info('本次抓取结束，时间是:{curtime}'.format(curtime=time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime())))
            if is_404(page):
                crawler.warning('url为{url}的连接不存在'.format(url=url))
                return ''
            if not is_complete(page):
                time.sleep(excp_interal)
                try:
                    page = session.get(url, headers=headers, timeout=time_out, verify=False).text. \
                        encode('utf-8', 'ignore').decode('utf-8')
                except Exception as why:
                    crawler.error(why)
                    return ''
    except requests.exceptions.ReadTimeout:
        crawler.warning('抓取{url}时连接目标服务器超时'.format(url=url))
        time.sleep(excp_interal)
        return ''
    except requests.exceptions.ConnectionError as e:
        crawler.warning('目标服务器拒绝连接，程序休眠1分钟,具体异常信息为:{e}'.format(e=e))
        time.sleep(excp_interal)
        return ''
    else:
        return page
