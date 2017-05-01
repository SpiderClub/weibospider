# -*-coding:utf-8 -*-
import json
import time
from headers import headers
from page_get.basic import get_page
from page_parse import basic
from db import spread_original_dao
from page_parse import wbparse
from entities.spread_other_cache import SpreadOtherCache
from page_get import status
from page_get import user
from db import spread_other_dao, weibosearch_dao
from logger.log import crawler, parser
from config.conf import get_max_page


page_max = get_max_page()


def _get_current_reposts(url, session, weibo_mid):
    """
    修改过后的抓取主程序，由于微博频率限制比较严格，目前只抓取当前微博及其子微博，不抓取源微博
    """
    spread_other_caches = list()
    spread_others = list()
    spread_other_and_caches = list()

    html = get_page(url, session, headers)
    reposts = wbparse.get_repostcounts(html)
    comments = wbparse.get_commentcounts(html)

    # 更新weibo_search_data表中的转发数、评论数
    weibosearch_dao.update_repost_comment(mid=weibo_mid, reposts=reposts, comments=comments)

    if not basic.is_404(html):
        root_url = url
        mid = wbparse.get_mid(html)
        user_id = wbparse.get_userid(html)
        user_name = wbparse.get_username(html)
        post_time = wbparse.get_statustime(html)
        device = wbparse.get_statussource(html)
        comments_count = wbparse.get_commentcounts(html)
        reposts_count = wbparse.get_repostcounts(html)
        root_user = user.get_profile(user_id, session, headers)

        spread_original_dao.save(root_user, mid, post_time, device, reposts_count, comments_count, root_url)

        crawler.info('该微博转发数为{counts}'.format(counts=reposts_count))

        if reposts_count > 0:
            base_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={mid}&page={currpage}'
            soc = SpreadOtherCache()
            soc.set_id(user_id)
            soc.set_name(user_name)
            spread_other_caches.append(soc)
            page = 1
            ajax_url = base_url.format(mid=mid, currpage=page)
            source = get_page(ajax_url, session, headers, False)

            crawler.info('本次转发信息url为：' + ajax_url)

            try:
                repost_json = json.loads(source)
                total_page = int(repost_json['data']['page']['totalpage'])
            except Exception as why:
                parser.error('{url}使用json解析转发信息出现异常，具体信息为:{why}'.format(url=ajax_url, why=why))
            else:
                page = total_page
                page_counter = 0

                while page > 0 and page_counter < page_max:
                    ajax_url = base_url.format(mid=mid, currpage=page)
                    repost_info = get_page(ajax_url, session, headers, False)
                    try:
                        repost_json = json.loads(repost_info)
                        repost_html = repost_json['data']['html']
                    except Exception as why:
                        parser.error('{url}使用json解析转发信息出现异常，具体信息为:{why}'.format(url=ajax_url, why=why))
                    else:
                        repost_urls = wbparse.get_reposturls(repost_html)

                        # 转发节点排序逻辑
                        for repost_url in repost_urls:
                            repost_cont = status.get_status_info(repost_url, session, user_id, user_name, headers, mid)

                            if repost_cont is not None:
                                spread_other_and_caches.append(repost_cont)

                        for soac in spread_other_and_caches:
                            if soac.get_so().id != '':
                                spread_others.append(soac.get_so())
                                spread_other_caches.append(soac.get_soc())
                    finally:
                        print('当前位于第{currpage}页'.format(currpage=page))
                        page -= 1
                        page_counter += 1

                for so in spread_others:
                    if so.verify_type == '':
                        so.verify_type = 0

                    for i in spread_other_caches:
                        if so.upper_user_name == i.get_name():
                            so.upper_user_id = i.get_id()
                            break
                        else:
                            so.upper_user_id = user_id

                spread_others = list(set(spread_others))

                spread_other_dao.save(spread_others)
                crawler.info('一共获取了{num}条转发信息,该条微博的转发信息已经采集完成'.format(num=len(spread_others)))
    else:
        crawler.info('{url}为404页面'.format(url=url))


def get_all(d):
    while not d:
        crawler.info('现在还未得到有效的session')
        time.sleep(60)

    datas = weibosearch_dao.get_crawl_urls()
    crawler.info('一共获取到{len}条需要抓取的微博'.format(len=len(datas)))

    for data in datas:
        # session放在里面是为了防止某个抓取队列太长或者转发微博太多
        session = d.get('session')

        crawler.info('正在抓取url为{url}的微博'.format(url=data['url']))
        _get_current_reposts(data['url'], session, data['mid'])
        weibosearch_dao.update_weibo_url(data['mid'])

    crawler.info('本次抓取结束')
