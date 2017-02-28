# -*-coding:utf-8 -*-
import json, logging, os
from gl import headers, count, page_max
from do_dataget.basic import get_page
from do_dataprocess import basic
from db_operation import spread_original_dao
from do_dataprocess.do_statusprocess import status_parse
from weibo_entities.spread_other_cache import SpreadOtherCache
from do_dataget import get_statusinfo
from do_dataget import get_userinfo
from db_operation import spread_other_dao, weibosearch_dao
from logger.log import other


def _get_reposts(url, session, weibo_mid):
    """
    抓取主程序
    解析源微博，并保存；得到转发微博信息
    注意判断404页面，同理个人资料抓取程序也需要做同样的判断
    :param url:
    :param session:
    :return:
    """
    spread_other_caches = []
    spread_others = []
    spread_other_and_caches = []

    html = get_page(url, session, headers)
    reposts_count = status_parse.get_repostcounts(html)
    weibosearch_dao.update_weibo_repost(weibo_mid, reposts_count)

    if not basic.is_404(html):
        if not status_parse.is_root(html):
            print('该微博不是源微博，现在从源微博开始爬取')
            root_url = status_parse.get_rooturl(url, html)
            if root_url != '':
                html = get_page(root_url, session, headers)
                if basic.is_404(html):
                    print('源微博已经找不到了')
                    return

        mid = status_parse.get_orignalmid(html)
        user_id = status_parse.get_userid(html)
        user_name = status_parse.get_username(html)
        post_time = status_parse.get_statustime(html)
        device = status_parse.get_statussource(html)
        comments_count = status_parse.get_commentcounts(html)
        reposts_count = status_parse.get_repostcounts(html)
        root_user = get_userinfo.get_profile(user_id, session, headers)

        # 以下代码是因为测试反爬虫机制注释掉的
        rs = spread_original_dao.save(root_user, mid, post_time, device, reposts_count, comments_count, root_url)
        #
        # if rs is False:
        #     print('源微博的扩散信息已经获取过了')
        #     return

        print('转发数为{counts}'.format(counts=reposts_count))

        if reposts_count > 0:
            base_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={mid}&page={currpage}'
            soc = SpreadOtherCache()
            soc.set_id(user_id)
            soc.set_name(user_name)
            spread_other_caches.append(soc)
            page = 1
            ajax_url = base_url.format(mid=mid, currpage=page)
            source = get_page(ajax_url, session, headers, False)
            print('本次转发信息url为：' + ajax_url)

            try:
                repost_json = json.loads(source)
                total_page = int(repost_json['data']['page']['totalpage'])
            except Exception as why:
                print('使用json解析转发信息出现异常，具体信息为:{why}'.format(why=why))
                print('本次返回的转发信息为{info}'.format(info=source))
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
                        print('使用json解析转发信息出现异常，具体信息为:{why}'.format(why=why))
                        print('本次返回的转发信息为{info}'.format(info=source))
                    else:
                        repost_urls = status_parse.get_reposturls(repost_html)

                        for repost_url in repost_urls:
                            repost_cont = get_statusinfo.get_status_info(repost_url, session, user_id, user_name,
                                                                         headers)

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
                    for i in spread_other_caches:
                        if so.upper_user_name == i.get_name():
                            so.upper_user_id = i.get_id()
                            break
                        if so.verify_type == '':
                            so.verify_type = 0
                        else:
                            so.upper_user_id = user_id

                spread_others = list(set(spread_others))
                # 以下代码是研究反爬虫机制而注释掉的
                #  spread_other_dao.save(spread_others)
                print('一共获取了{num}条转发信息'.format(num=len(spread_others)))
                print('该条微博的转发信息已经采集完成')

    else:
        logging.info('{url}为404页面'.format(url=url))
        print('该微博{url}已经被删除了'.format(url=url))


def _get_current_reposts(url, session, weibo_mid):
    """
    修改过后的抓取主程序，由于微博频率限制比较严格，目前只抓取当前微博及其子微博，不抓取源微波
    :param url:
    :param session:
    :return:
    """
    spread_other_caches = []
    spread_others = []
    spread_other_and_caches = []

    html = get_page(url, session, headers)
    reposts_count = status_parse.get_repostcounts(html)
    # 更新weibo_search_data表中的转发数、评论数
    weibosearch_dao.update_weibo_repost(weibo_mid, reposts_count)

    if not basic.is_404(html):
        root_url = url
        mid = status_parse.get_mid(html)
        user_id = status_parse.get_userid(html)
        user_name = status_parse.get_username(html)
        post_time = status_parse.get_statustime(html)
        device = status_parse.get_statussource(html)
        comments_count = status_parse.get_commentcounts(html)
        reposts_count = status_parse.get_repostcounts(html)
        root_user = get_userinfo.get_profile(user_id, session, headers)

        spread_original_dao.save(root_user, mid, post_time, device, reposts_count, comments_count, root_url)
        print('转发数为{counts}'.format(counts=reposts_count))

        if reposts_count > 0:
            base_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={mid}&page={currpage}'
            soc = SpreadOtherCache()
            soc.set_id(user_id)
            soc.set_name(user_name)
            spread_other_caches.append(soc)
            page = 1
            ajax_url = base_url.format(mid=mid, currpage=page)
            source = get_page(ajax_url, session, headers, False)
            print('本次转发信息url为：' + ajax_url)

            try:
                repost_json = json.loads(source)
                total_page = int(repost_json['data']['page']['totalpage'])
            except Exception as why:
                print('使用json解析转发信息出现异常，具体信息为:{why}'.format(why=why))
                print('本次返回的转发信息为{info}'.format(info=source))
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
                        print('使用json解析转发信息出现异常，具体信息为:{why}'.format(why=why))
                        print('本次返回的转发信息为{info}'.format(info=source))
                    else:
                        repost_urls = status_parse.get_reposturls(repost_html)

                        for repost_url in repost_urls:
                            repost_cont = get_statusinfo.get_status_info(repost_url, session, user_id, user_name, headers, mid)

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
                print('一共获取了{num}条转发信息'.format(num=len(spread_others)))
                print('该条微博的转发信息已经采集完成')
    else:
        logging.info('{url}为404页面'.format(url=url))
        print('该微博{url}已经被删除了'.format(url=url))


def get_all(d):
    datas = weibosearch_dao.get_crawl_urls()
    other.info('一共获取到{len}条需要抓取的微博'.format(len=len(datas)))
    for data in datas:
        # session放在里面是为了防止某个抓取队列太长或者转发微博太多
        session = d['session']
        logging.info('正在抓取url为{url}的微博'.format(url=data['url']))
        _get_current_reposts(data['url'], session, data['mid'])
        # 这样处理会导致某些微博给漏掉
        weibosearch_dao.update_weibo_url(data['mid'])

    logging.info('本次启动一共抓取了{count}个页面'.format(count=count))
