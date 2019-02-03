import re
import urllib.parse
from datetime import datetime

from bs4 import BeautifulSoup

from logger import parser
from page_get import status
from utils import url_filter
from db.models import WeiboData
from decorators import parse_decorator
from tasks.workers import app
from config import (
    get_crawling_mode, get_images_allow, get_images_path)


CRAWLING_MODE = get_crawling_mode()
IMG_ALLOW = get_images_allow()
IMG_PATH = get_images_path()


@parse_decorator('')
def _search_page_parse(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'view\((.*)\)')
    for script in scripts:
        m = pattern.search(str(script))
        # 这个判断不全面，对于json编码的可以成功，对于直接返回的不会成功
        if m and 'pl_weibo_direct' in script.string and 'S_line1' in script.string:
            search_cont = m.group(1)
            pattern2 = re.compile(r'"html":"(.*)"}$')
            m2 = pattern2.search(search_cont)
            if m2:
                return m2.group(1).encode('utf-8', 'ignore').decode('unicode-escape', 'ignore').replace('\\', '')
    return ''


def get_feed_info(feed_infos, goal):
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

    try:
        wb_data.weibo_id = each['mid']
    except (AttributeError, IndexError, TypeError):
        parser.error('Failed to get weibo id, the page source is {}'.format(html))
        return None

    imgs = list()
    imgs_url = list()
    try:
        imgs = str(each.find(attrs={'node-type': 'feed_list_media_prev'}).find_all('li'))
        imgs_url = list(map(url_filter, re.findall(r"src=\"(.+?)\"", imgs)))
        wb_data.weibo_img = ';'.join(imgs_url)
    except Exception:
        wb_data.weibo_img = ''

    if IMG_ALLOW and imgs and imgs_url:
        app.send_task('tasks.downloader.download_img_task', args=(wb_data.weibo_id, imgs_url),
                      queue='download_queue', routing_key='for_download')
        wb_data.weibo_img_path = IMG_PATH
    else:
        wb_data.weibo_img_path = ''

    # todo 没找到vedio的测试数据
    try:
        a_tag = str(each.find(attrs={'node-type': 'feed_list_media_prev'}).find_all('a'))
        extracted_url = urllib.parse.unquote(re.findall(r"full_url=(.+?)&amp;", a_tag)[0])
        wb_data.weibo_video = url_filter(extracted_url)
    except Exception:
        wb_data.weibo_video = ''

    try:
        wb_data.device = each.find(attrs={'class': 'from'}).find(attrs={'rel': 'nofollow'}).text
    except AttributeError:
        wb_data.device = ''

    try:
        # todo 日期格式化,会有今日XXX，X分钟前等噪音
        wb_data.create_time = each.find(attrs={'class': 'from'}).find(attrs={'target': '_blank'}).text.strip()
        wb_data.weibo_url = 'https:'+each.find(attrs={'class': 'from'}).find(attrs={'target': '_blank'})['href']
        wb_data.uid = each.find(attrs={'class': 'from'}).find(attrs={'target': '_blank'})['href'].split('/')[3]
    except (AttributeError, KeyError):
        wb_data.create_time = ''
        wb_data.weibo_url = ''
        wb_data.weibo_uid = ''

    try:
        wb_data.repost_num = int(each.find(attrs={'class': 'card-act'}).find_all('li')[0].find('a').text.split('/')[-1])
    except (AttributeError, ValueError):
        wb_data.repost_num = 0
    try:
        wb_data.comment_num = int(each.find(attrs={'class': 'card-act'}).find_all('li')[1].find('a').text.split('/')[-1])
    except (AttributeError, ValueError):
        wb_data.comment_num = 0
    try:
        wb_data.praise_num = int(each.find(attrs={'class': 'card-act'}).find_all('li')[2].find('a').find('em').text)
    except (AttributeError, ValueError):
        wb_data.praise_num = 0

    if '展开全文' in str(each):
        is_all_cont = 1
        try:
            wb_data.weibo_cont = each.find(attrs={'node-type': 'feed_list_content_full'}).text.strip()
        except Exception as why:
            parser.error('Failed to get weibo cont, the error is {}, the page source is {}'.format(why, html))
            return None
    else:
        is_all_cont = 1
        try:
            wb_data.weibo_cont = each.find(attrs={'node-type': 'feed_list_content'}).text.strip()
        except Exception as why:
            parser.error('Failed to get weibo cont, the error is {}, the page source is {}'.format(why, html))
            return None
    return wb_data, is_all_cont


@parse_decorator([])
def get_search_info(html):
    """
    :param html: response content for search with login
    :return: search results
    """
    # 搜索结果可能有两种方式，一种是直接返回的，一种是编码过后的
    content = _search_page_parse(html) if '举报' in html else html
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




