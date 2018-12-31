import json
import html as htmllib

from bs4 import BeautifulSoup

from logger import parser
from db.models import WeiboPraise
from decorators import parse_decorator


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
        parser.error('Get total page error, the reason is {}'.format(e))
        page_count = 1

    return page_count


@parse_decorator([])
def get_praise_list(html:str, wb_id:str):
    """[get praise list]
    
    Arguments:
        html {str} -- [web page]
        wb_id {str} -- [weibo mid]
    
    Raises:
        in -- [can't get wanted dom]
    
    Returns:
        WeiboPraise list -- [list contains praises in this html]
        ext_param -- [extra parameters to get next page]
    """

    cont = get_html_cont(html)
    if not cont:
        return list(), ''

    soup = BeautifulSoup(cont, 'html.parser')
    praise_list = list()
    praises = soup.find_all(attrs={'class': 'list_li S_line1 clearfix'})
    # pattern = re.compile(r'<li uid=\\"\d{10}\\">')
    # praises = pattern.findall(cont)

    for praise in praises:
        try:
            user_id = praise.find('img').get('usercard')[3:]
            wb_praise = WeiboPraise(user_id, wb_id)
        except Exception as e:
            parser.error('解析点赞失败，具体信息是{}'.format(e))
        else:
            praise_list.append(wb_praise)

    like_loading = soup.find(attrs={'node-type': 'like_loading'})
    feed_like_more = soup.find(attrs={'action-type': 'feed_like_more'})
    if like_loading:
        action_data = like_loading.get('action-data', '')
    elif feed_like_more:
        action_data = feed_like_more.get('action-data', '')
    else:
        action_data = ''
    ext_param = htmllib.unescape(action_data)

    return praise_list, ext_param
