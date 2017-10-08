import re
import json

from bs4 import BeautifulSoup

from decorators import parse_decorator
from logger import parser


@parse_decorator('')
def get_userid(html):
    pattern = re.compile(r'\$CONFIG\[\'oid\'\]=\'(.*)\';')
    m = pattern.search(html)
    return m.group(1) if m else ''


@parse_decorator('')
def get_username(html):
    pattern = re.compile(r'\$CONFIG\[\'onick\'\]=\'(.*)\';')
    m = pattern.search(html)
    return m.group(1) if m else ''


@parse_decorator('')
def get_userdomain(html):
    """
    :param html:
    :return:用户类型
    """
    pattern = re.compile(r'\$CONFIG\[\'domain\'\]=\'(.*)\';')
    m = pattern.search(html)
    return m.group(1) if m else ''


@parse_decorator('')
def _get_statushtml(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    for script in scripts:
        try:
            m = pattern.search(script.string)
            if m and 'pl.content.weiboDetail.index' in script.string:
                all_info = m.group(1)
                # TODO 留意这里可能发生异常
                cont = json.loads(all_info)['html']
        except TypeError:
            return ''
        except Exception as e:
            parser.error('__get__statushtml()错误,具体错误是'.format(e=e))
            parser.error('网页代码为{page}'.format(page=html))
    return cont


@parse_decorator('')
def get_mid(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, 'html.parser')
    try:
        return soup.find(attrs={'action-type': 'feed_list_item'})['mid']
    except TypeError:
        mid_pattern = r'mid=(\d+)'
        mid_matcher = re.search(mid_pattern, html)
        return mid_matcher.group(1) if mid_matcher else ''
    except Exception as e:
        parser.error('get_mid()发生异常,具体异常为{e}'.format(e=e))


@parse_decorator('')
def get_orignalmid(html):
    """
    :return: 如果本来就是源微博，则返回微博id,否则返回源微博id
    """
    if is_root(html):
        return get_mid(html)
    else:
        cont = _get_statushtml(html)
        soup = BeautifulSoup(cont, 'html.parser')
        return soup.find(attrs={'action-type': 'feed_list_item'})['omid']


@parse_decorator('')
def get_statussource(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, "html.parser")
    # 不同模版的不同解析方法
    try:
        return soup.find(attrs={'action-type': 'app_source'}).text
    except AttributeError:
        try:
            return soup.find(attrs={'class': 'WB_from S_txt2'}).find_all('a')[1].text
        except Exception:
            return ''


@parse_decorator('')
def get_statustime(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, "html.parser")
    try:
        return soup.find(attrs={'node-type': 'feed_list_item_date'})['title']
    except TypeError:
        return ''


@parse_decorator(0)
def get_repostcounts(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, "html.parser")
    try:
        reposts = soup.find(attrs={'node-type': 'forward_btn_text'}).find('span').find('em').find_next_sibling().text
        if reposts == '转发':
            return 0
        counts = int(reposts)
        return counts
    except (ValueError, AttributeError) as e:
        parser.error(e)
        return 0


@parse_decorator(0)
def get_commentcounts(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, "html.parser")
    try:
        comments = soup.find(attrs={'node-type': 'comment_btn_text'}).find('span').find('em').find_next_sibling().text
        if comments == '评论':
            return 0
        counts = int(comments)
        return counts
    except (ValueError, AttributeError) as e:
        parser.error(e)
        return 0


@parse_decorator(0)
def get_likecounts(html):
    cont = _get_statushtml(html)
    soup = BeautifulSoup(cont, "html.parser")
    try:
        if is_root(html):
            likes = soup.find(attrs={'node-type': 'like_status'}).find_all('em')[1].text
        else:
            likes = soup.find_all(attrs={'node-type': 'like_status'})[1].find_all('em')[1].text
        if likes == '赞':
            return 0
        else:
            return int(likes)
    except (ValueError, AttributeError) as e:
        parser.error(e)
        return 0


def is_root(html):
    try:
        return False if 'omid=' in html else True
    except TypeError:
        return True


@parse_decorator('')
def get_rooturl(cururl, html):
    if is_root(html):
        return cururl
    else:
        cont = _get_statushtml(html)
        if cont == '':
            return ''
        soup = BeautifulSoup(cont, 'html.parser')
        try:
            url = 'http://weibo.com'+soup.find(attrs={'node-type': 'feed_list_forwardContent'}).find(attrs={'class': 'WB_from'}).find(attrs={'class': 'S_txt2'})['href']
        except TypeError:
            return ''
        except AttributeError:
            print('解析错误')
            return ''
        except KeyError:
            return ''
        else:
            return url


@parse_decorator([])
def get_reposturls(repostinfo):
    """
    :param repostinfo: 转发信息
    :return: 获取所有转发url
    """
    try:
        repost_urls = []
        prestring = 'http://weibo.com'
        soup = BeautifulSoup(repostinfo, 'html.parser')
        contents = soup.find_all(attrs={'node-type': 'feed_list_item_date'})
        for content in contents:
            repost_urls.append(prestring+content['href'])
        return repost_urls
    except AttributeError:
        return []


def get_upperusername(html, defaultname):
    cont = _get_statushtml(html)
    if 'type=atname' in cont:
        try:
            soup = BeautifulSoup(cont, 'html.parser')
            content = soup.find(attrs={'node-type': 'feed_list_content'}).find(attrs={'render': 'ext',
                                                                                      'extra-data': 'type=atname'}).text
            return content[1:]
        except AttributeError:
            return defaultname
        except Exception as e:
            parser.error(e)
            return defaultname
    else:
        return defaultname
