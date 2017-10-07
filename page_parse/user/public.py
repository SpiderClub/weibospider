import re
import json

from bs4 import BeautifulSoup

from page_parse import status
from decorators import parse_decorator
from db.models import UserRelation
from utils import url_filter
from db.dao import UserRelationOper


def get_userid(html):
    return status.get_userid(html)


def get_username(html):
    return status.get_username(html)


def get_userdomain(html):
    return status.get_userdomain(html)


@parse_decorator('')
def _get_header(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'pl.header.head.index' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
    return cont


def get_verifytype(html):
    """
    :param html: page source
    :return: 0 stands for unauthorized，1 stands for persional authentication，2 stands for enterprise authentication
    """
    if 'icon_pf_approve_co' in html:
        return 2
    elif 'icon_pf_approve' in html:
        return 1
    else:
        return 0


@parse_decorator('')
def get_verifyreason(html, verify_type):
    """
    details for authentication
    :param html: page source
    :param verify_type: authentication type
    :return: authentication info
    """
    if verify_type == 1 or verify_type == 2:
        soup = BeautifulSoup(_get_header(html), 'html.parser')
        return soup.find(attrs={'class': 'pf_intro'})['title']
    else:
        return ''


@parse_decorator('')
def get_headimg(html):
    """
    Get the head img url of current user
    :param html: page source
    :return: head img url
    """
    soup = BeautifulSoup(_get_header(html), 'html.parser')
    try:
        headimg = url_filter(soup.find(attrs={'class': 'photo_wrap'}).find(attrs={'class': 'photo'})['src'])
    except AttributeError:
        headimg = ''
    return headimg


@parse_decorator('')
def get_left(html):
    """
    The left part of the page, which is public
    """
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    l_id = ''
    # first ensure the left part
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'WB_frame_b' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
            lsoup = BeautifulSoup(cont, 'html.parser')
            l_id = lsoup.find(attrs={'class': 'WB_frame_b'}).div['id']
    for script in scripts:
        m = pattern.search(script.string)
        if m and l_id in script.string:
            all_info = m.group(1)
            try:
                cont = json.loads(all_info)['html']
            except KeyError:
                return ''
    return cont


@parse_decorator('')
def get_right(html):
    """
    Parse the right part of user detail
    :param html: page source
    :return: the right part of user info page
    """
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    # first ensure right part,enterprise users may have two r_id
    rids = []
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'WB_frame_c' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info).get('html', '')
            if not cont:
                return ''
            rsoup = BeautifulSoup(cont, 'html.parser')
            r_ids = rsoup.find(attrs={'class': 'WB_frame_c'}).find_all('div')
            for r in r_ids:
                rids.append(r['id'])
    for script in scripts:
        for r_id in rids:
            m = pattern.search(script.string)
            if m and r_id in script.string:
                all_info = m.group(1)
                cont += json.loads(all_info).get('html', '')

    return cont


@parse_decorator(0)
def get_level(html):
    """
    Get the level of users
    """
    pattern = '<span>Lv.(.*?)<\\\/span>'
    rs = re.search(pattern, html)
    if rs:
        return rs.group(1)
    else:
        return 0


@parse_decorator([])
def get_fans_or_follows(html, uid, type):
    """
    Get fans or follows and store their relationships
    :param html: current page source
    :param uid: current user id
    :param type: type of relations, 1 stands for fans，2 stands for follows
    :return: list of fans or followers
    """
    if html == '':
        return list()

    pattern = re.compile(r'FM.view\((.*)\)')
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')

    user_ids = list()
    relations = list()
    for script in scripts:
        m = re.search(pattern, script.string)

        if m and 'pl.content.followTab.index' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info).get('html', '')
            soup = BeautifulSoup(cont, 'html.parser')
            follows = soup.find(attrs={'class': 'follow_box'}).find_all(attrs={'class': 'follow_item'})
            pattern = 'uid=(.*?)&'
            for follow in follows:
                m = re.search(pattern, str(follow))
                if m:
                    r = m.group(1)
                    # filter invalid ids
                    if r.isdigit():
                        user_ids.append(r)
                        relations.append(UserRelation(uid, r, type))

    UserRelationOper.add_all(relations)
    return user_ids


def get_max_crawl_pages(html):
    """
    Get the max page we can crawl
    :param html: current page source
    :return: max page number we can crawl
    """
    if html == '':
        return 1

    pattern = re.compile(r'FM.view\((.*)\)')
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    length = 1

    for script in scripts:
        m = re.search(pattern, script.string)

        if m and 'pl.content.followTab.index' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info).get('html', '')
            soup = BeautifulSoup(cont, 'html.parser')
            pattern = 'uid=(.*?)&'

            if 'pageList' in cont:
                urls2 = soup.find(attrs={'node-type': 'pageList'}).find_all(attrs={
                    'class': 'page S_txt1', 'bpfilter': 'page'})
                length += len(urls2)
    return length
