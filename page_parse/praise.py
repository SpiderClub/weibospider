import json

from bs4 import BeautifulSoup

from logger import parser_logger
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
        parser_logger.error('Get total page error, the reason is {}'.format(e))
        page_count = 1

    return page_count


@parse_decorator([])
def get_praise_list(html, wb_id):
    """
    获取点赞列表
    :param html: 
    :param wb_id: 
    :return: 
    """
    cont = get_html_cont(html)
    if not cont:
        return list()

    soup = BeautifulSoup(cont, 'html.parser')
    praise_list = list()
    praises = soup.find_all('li')
    # pattern = re.compile(r'<li uid=\\"\d{10}\\">')
    # praises = pattern.findall(cont)

    for praise in praises:
        wb_praise = WeiboPraise()
        try:
            wb_praise.user_id = praise['uid']
            wb_praise.weibo_id = wb_id
        except Exception as e:
            parser_logger.error('解析点赞失败，具体信息是{}'.format(e))
        else:
            praise_list.append(wb_praise)

    return praise_list