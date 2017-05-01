# -*-coding:utf-8 -*-
import json
from page_parse import basic
from tasks.workers import app
from page_get import user, status
from db import spread_original_dao
from page_get.basic import get_page
from config.conf import get_max_page
from logger.log import crawler, parser
from page_parse import status as parse_status
from db import spread_other_dao, weibosearch_dao
from entities.spread_other_cache import SpreadOtherCache


page_max = get_max_page()
base_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={mid}&page={currpage}'


# 获取当前微博被转发相关信息
def _get_current_source(url, wb_mid):
    """
    :param url: 当前微博url
    :param wb_mid: 当前微博mid
    :return: 转发数，微博用户id,用户名
    """
    html = get_page(url)
    if not html or basic.is_404(html):
        return None

    reposts = parse_status.get_repostcounts(html)
    comments = parse_status.get_commentcounts(html)

    # 更新weibo_search_data表中的转发数、评论数
    weibosearch_dao.update_repost_comment(mid=wb_mid, reposts=reposts, comments=comments)

    root_url = url
    user_id = parse_status.get_userid(html)
    user_name = parse_status.get_username(html)
    post_time = parse_status.get_statustime(html)
    device = parse_status.get_statussource(html)
    comments_count = parse_status.get_commentcounts(html)
    reposts_count = parse_status.get_repostcounts(html)
    root_user = user.get_profile(user_id)
    # 源微博的相关信息存储
    spread_original_dao.save(root_user, wb_mid, post_time, device, reposts_count, comments_count, root_url)

    crawler.info('该微博转发数为{counts}'.format(counts=reposts_count))
    return reposts_count, user_id, user_name


def _get_total_page(wb_mid):
    page = 1
    ajax_url = base_url.format(mid=wb_mid, currpage=page)
    source = get_page(ajax_url, False)

    if source == '':
        crawler.error('本次转发url{}抓取出错'.format(ajax_url))
        return 0

    crawler.info('本次转发信息url为{}'.format(ajax_url))

    try:
        repost_json = json.loads(source)
        total_page = int(repost_json['data']['page']['totalpage'])
    except Exception as why:
        parser.error('{url}使用json解析转发信息出现异常，具体信息为:{why}'.format(url=ajax_url, why=why))
        return 0
    else:
        return total_page


def _save_spread_other(spread_others, spread_other_caches, uid):
    for so in spread_others:
        if so.verify_type == '':
            so.verify_type = 0

        for i in spread_other_caches:
            if so.upper_user_name == i.get_name():
                so.upper_user_id = i.get_id()
                break
            else:
                # 如果在回溯父节点的时候发生异常，那么就让父节点为默认节点
                so.upper_user_id = uid

    spread_others = list(set(spread_others))
    spread_other_dao.save(spread_others)


# 微博转发数据抓取主逻辑
def _crawl_loop(page, page_counter, mid, uid, user_name, spread_other_and_caches, spread_others, spread_other_caches):
    while page > 0 and page_counter < page_max:
        ajax_url = base_url.format(mid=mid, currpage=page)
        repost_info = get_page(ajax_url, False)
        try:
            repost_json = json.loads(repost_info)
            repost_html = repost_json['data']['html']
        except Exception as why:
            # 如果出现异常，默认不抓该ajax_url对应的微博信息
            parser.error('{url}使用json解析转发信息出现异常，具体信息为:{why}'.format(url=ajax_url, why=why))
        else:
            repost_urls = parse_status.get_reposturls(repost_html)

            # 转发节点排序逻辑
            # todo 不通过repost_urls去获取转发微博的相关信息，验证扩散效果是否相同
            for repost_url in repost_urls:
                repost_cont = status.get_status_info(repost_url, uid, user_name, mid)
                if repost_cont is not None:
                    spread_other_and_caches.append(repost_cont)

            for soac in spread_other_and_caches:
                if soac.get_so().id != '':
                    spread_others.append(soac.get_so())
                    spread_other_caches.append(soac.get_soc())
        finally:
            print('当前位于第{}页'.format(page))
            page -= 1
            page_counter += 1


# todo 划分为更细粒度的任务(将每条转发任务分布给各个机器)
@app.task
def get_current_reposts(url, weibo_mid):
    """
    抓取主程序，抓取当前微博及其子微博，不向上追溯源微博
    """
    crawler.info('正在抓取url为{}的微博'.format(url))
    spread_other_caches = list()
    spread_others = list()
    spread_other_and_caches = list()

    result = _get_current_source(url, weibo_mid)
    if result is None:
        weibosearch_dao.update_weibo_url(weibo_mid, 2)
        return
    reposts_count, user_id, user_name = result

    if reposts_count > 0:
        soc = SpreadOtherCache()
        soc.set_id(user_id)
        soc.set_name(user_name)
        spread_other_caches.append(soc)

        page = _get_total_page(weibo_mid)
        if page == 0:
            weibosearch_dao.update_weibo_url(weibo_mid, 2)
            return

        page_counter = 0
        _crawl_loop(page, page_counter, weibo_mid, user_id, user_name, spread_other_and_caches,
                    spread_others, spread_other_caches)
        _save_spread_other(spread_others, spread_other_caches, user_id)
        crawler.info('一共获取了{num}条转发信息,该条微博的转发信息已经采集完成'.format(num=len(spread_others)))

    weibosearch_dao.update_weibo_url(weibo_mid, 1)


# todo 添加为定时任务，但是要考虑到在上一次get_all()执行完了才执行下一次的get_all;验证如果并发数为1，是否就会依次执行？
# todo 如何判断一轮任务已经完成？根据一轮任务完成时间，定义一个间隔执行第二轮任务？如何让该函数阻塞执行？
@app.task
def excute_repost_task():
    datas = weibosearch_dao.get_crawl_urls()
    crawler.info('一共获取到{len}条需要抓取的微博'.format(len=len(datas)))
    # 把抓取任务分发到各个机器上执行
    for data in datas:
        app.send_task('tasks.repost.get_current_reposts', args=(data['url'], data['mid']))

    crawler.info('本次任务分发完成')
