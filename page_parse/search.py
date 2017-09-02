# -*-coding:utf-8 -*-
import re
import urllib.parse
from datetime import datetime


from bs4 import BeautifulSoup

from page_get import status
from logger.log import parser
from db.models import WeiboData
from config.conf import get_crawling_mode
from decorators.decorator import parse_decorator


ORIGIN = 'http'
PROTOCOL = 'https'
USER_PATTERN = r'id=(\d+)&u'
CRAWLING_MODE = get_crawling_mode()


@parse_decorator('')
def _search_page_parse(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'view\((.*)\)')
    for script in scripts:
        m = pattern.search(str(script))
        # 这个判断不全面，对于json编码的可以成功，对于直接返回的不会成功
        if m and 'pl_weibo_direct' in script.string and 'S_txt1' in script.string:
            search_cont = m.group(1)
            pattern2 = re.compile(r'"html":"(.*)"}$')
            m2 = pattern2.search(search_cont)
            if m2:
                return m2.group(1).encode('utf-8', 'ignore').decode('unicode-escape', 'ignore').replace('\\', '')
    return ''


def get_feed_info(feed_infos,goal):
    info_num = None
    for info in feed_infos:
        if goal in info.text:
            info_num = info.text.replace(goal, '')
            break
    if info_num is None:
        parser.error('unexcept template:{}'.format(feed_infos))
    return int(info_num)


@parse_decorator(None)
def get_weibo_info(each, html):
    wb_data = WeiboData()
    user_cont = each.find(attrs={'class': 'face'})
    user_info = user_cont.find('a')
    m = re.match(USER_PATTERN, user_info.img.get('usercard'))

    if m:
        wb_data.uid = m.group(1)
    else:
        parser.warning("fail to get user'sid, the page source is{}".format(html))
        return None
    try:
        wb_data.weibo_id = each.find(attrs={'class': 'WB_screen'}).find('a').get('action-data')[4:]
    except (AttributeError, IndexError, TypeError):
        return None

    try:
        wb_data.weibo_url = each.find(attrs={'node-type': 'feed_list_item_date'})['href']
    except Exception as e:
        parser.error('fail to get weibo url, the error is {}, the source page is {}'.format(e, html))
        return None

    def url_filter(url):
        return ':'.join([PROTOCOL, url]) if PROTOCOL not in url and ORIGIN not in url else url

    try:
        imgs = str(each.find(attrs={'node-type': 'feed_list_media_prev'}).find_all('li'))
        imgs_url = map(url_filter, re.findall(r"src=\"(.+?)\"", imgs))
        wb_data.weibo_img = ';'.join(imgs_url)
    except Exception:
        wb_data.weibo_img = ''

    try:
        a_tag = str(each.find(attrs={'node-type': 'feed_list_media_prev'}).find_all('a'))
        extracted_url = urllib.parse.unquote(re.findall(r"full_url=(.+?)&amp;", a_tag)[0])
        wb_data.weibo_video = url_filter(extracted_url)
    except Exception:
        wb_data.weibo_video = ''
    try:
        wb_data.device = each.find(attrs={'class': 'feed_from'}).find(attrs={'rel': 'nofollow'}).text
    except AttributeError:
        wb_data.device = ''

    try:
        create_time = each.find(attrs={'node-type': 'feed_list_item_date'})['date']
    except (AttributeError, KeyError):
        wb_data.create_time = ''
    else:
        create_time = int(create_time) / 1000  # 时间戳单位不同
        create_time = datetime.fromtimestamp(create_time)
        wb_data.create_time = create_time.strftime("%Y-%m-%d %H:%M")

    try:
        feed_action = each.find(attrs={'class': 'feed_action'})
    except Exception as why:
        parser.error('failt to get feed_action, the error is {},the page source is {}'.format(why, each))
    else:
        feed_infos = feed_action.find_all('li')
        try:
            wb_data.repost_num = get_feed_info(feed_infos, '转发')
        except (AttributeError, ValueError):
            wb_data.repost_num = 0
        try:
            wb_data.comment_num = get_feed_info(feed_infos, '评论')
        except (AttributeError, ValueError):
            wb_data.comment_num = 0
        try:
            wb_data.praise_num = int(feed_action.find(attrs={'action-type': 'feed_list_like'}).find('em').text)
        except (AttributeError, ValueError):
            wb_data.praise_num = 0

    try:
        wb_data.weibo_cont = each.find(attrs={'class': 'comment_txt'}).text.strip()
    except Exception as why:
        parser.error('fail to get weibo cont, the error is {}, the page source is {}'.format(why, html))
        return None

    if '展开全文' in str(each):
        is_all_cont = 0
    else:
        is_all_cont = 1
    return wb_data, is_all_cont


@parse_decorator(None)
def get_search_info(html):
    """
    通过搜索页的内容获取搜索结果
    :param html: 
    :return: 
    """
    # 搜索结果可能有两种方式，一种是直接返回的，一种是编码过后的
    content = _search_page_parse(html) if '举报' not in html else html

    if content == '':
        return list()
    # todo 这里用bs会导致某些信息不能被解析（参考../tests/fail.html），可参考使用xpath，考虑到成本，暂时不实现
    soup = BeautifulSoup(content.encode('utf-8', 'ignore').decode('utf-8'), "html.parser")

    feed_list = soup.find_all(attrs={'action-type': 'feed_list_item'})
    search_list = []
    for each in feed_list:
        r = get_weibo_info(each, html)
        if r is not None:
            wb_data = r[0]
            if r[1] == 0 and CRAWLING_MODE == 'accurate':
                weibo_cont = status.get_cont_of_weibo(wb_data.weibo_id)
                wb_data.weibo_cont = weibo_cont if weibo_cont else wb_data.weibo_cont
            search_list.append(wb_data)
    return search_list




