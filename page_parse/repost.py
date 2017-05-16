import json
from bs4 import BeautifulSoup
from logger.log import parser
from db.models import WeiboRepost
from db.redis_db import IdNames
from decorators.decorator import parse_decorator


repost_url = 'http://weibo.com{}'


@parse_decorator(1)
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
        parser.error('获取总也面出错，具体错误是{}'.format(e))
        page_count = 1

    return page_count


@parse_decorator(2)
def get_repost_list(html, mid):
    """
       获取转发列表
       :param html: 
       :param mid:
       :return: 
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
            wb_repost.weibo_url = repost_url.format(repost.find(attrs={'class': 'WB_from S_txt2'}).find('a').
                                                    get('href'))
            parents = repost.find(attrs={'class': 'WB_text'}).find(attrs={'node-type': 'text'})
            wb_repost.root_weibo_id = mid

            # 把当前转发的用户id和用户名存储到redis中，作为中间结果
            IdNames.store_id_name(wb_repost.user_name, wb_repost.user_id)

            if not parents:
                wb_repost.parent_user_name = ''
            else:
                try:
                    # 第一个即是最上层用户，由于拿不到上层用户的uid，只能拿昵称，但是昵称可以修改，所以入库前还是得把uid拿到
                    temp = parents.find(attrs={'extra-data': 'type=atname'})
                    if temp:
                        wb_repost.parent_user_name = temp.get('usercard')[5:]
                    else:
                        wb_repost.parent_user_name = ''
                except Exception as e:
                    parser.error('解析上层用户名发生错误，具体信息是{}'.format(e))
                    wb_repost.parent_user_name = ''

        except Exception as e:
            parser.error('解析评论失败，具体信息是{}'.format(e))
        else:
            repost_list.append(wb_repost)

    return repost_list