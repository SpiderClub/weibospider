import json

from bs4 import BeautifulSoup

from logger import parser
from db.models import WeiboRepost
from db.redis_db import IdNames
from decorators import parse_decorator


REPOST_URL = 'http://weibo.com{}'


@parse_decorator('')
def get_html_cont(html):
    cont = ''
    data = json.loads(html, encoding='utf-8').get('data', '')
    if data:
        cont = data.get('html', '')

    return cont


def get_total_page(html):
    try:
        page_count = json.loads(html, encoding='utf-8').get('data', '').get('page', '').get('totalpage', 1)
    except Exception as e:
        parser.error('Errors occurred when parsing total page of repost，specification is {}'.format(e))
        page_count = 1

    return page_count


@parse_decorator([])
def get_repost_list(html, mid):
    """
       Get repost details
       :param html: page source
       :param mid: weibo mid
       :return: list of repost infos
       """
    cont = get_html_cont(html)
    if not cont:
        return list()

    soup = BeautifulSoup(cont, 'html.parser')
    repost_list = list()
    reposts = soup.find_all(attrs={'action-type': 'feed_list_item'})

    for repost in reposts:
        wb_repost = WeiboRepost()
        try:
            repost_cont = repost.find(attrs={'class': 'WB_text'}).find(attrs={'node-type': 'text'}).text.strip().\
                split('//@')
            wb_repost.repost_cont = repost_cont[0].encode('gbk', 'ignore').decode('gbk', 'ignore')
            wb_repost.weibo_id = repost['mid']
            # TODO 将wb_repost.user_id加入待爬队列（seed_ids）
            wb_repost.user_id = repost.find(attrs={'class': 'WB_face W_fl'}).find('a').get('usercard')[3:]
            wb_repost.user_name = repost.find(attrs={'class': 'list_con'}).find(attrs={'class': 'WB_text'}).find('a').\
                text
            wb_repost.repost_time = repost.find(attrs={'class': 'WB_from S_txt2'}).find('a').get('title')
            wb_repost.weibo_url = REPOST_URL.format(repost.find(attrs={'class': 'WB_from S_txt2'}).find('a').
                                                    get('href'))
            parents = repost.find(attrs={'class': 'WB_text'}).find(attrs={'node-type': 'text'})
            wb_repost.root_weibo_id = mid

            # Save the current repost user's name and id as the middle result
            IdNames.store_id_name(wb_repost.user_name, wb_repost.user_id)

            if not parents:
                wb_repost.parent_user_name = ''
            else:
                try:
                    # We can't get the parent's uid, We can get the parent's nickname, but the name can be changed
                    temp = parents.find(attrs={'extra-data': 'type=atname'})
                    if temp:
                        wb_repost.parent_user_name = temp.get('usercard')[5:]
                    else:
                        wb_repost.parent_user_name = ''
                except Exception as e:
                    parser.error("error occurred when parsing the parent's name ，the detail is {}".format(e))
                    wb_repost.parent_user_name = ''

        except Exception as e:
            parser.error('repost parse error occurred，the detail is {}'.format(e))
        else:
            repost_list.append(wb_repost)

    return repost_list