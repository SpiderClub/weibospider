import json

from bs4 import BeautifulSoup

from logger import parser
from db.models import WeiboComment
from decorators import parse_decorator
from utils import parse_emoji

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
    except Exception:
        try:
            json.loads(html, encoding='utf-8').get('data', '').get('tag', '')
            page_count = 1
        except Exception as e:
            parser.error('Get total page error, the reason is {}'.format(e))
            page_count = 1

    return page_count


@parse_decorator('')
def get_next_url(html):
    """
    获取下一次应该访问的url
    :param html: 
    :return: 
    """
    cont = get_html_cont(html)
    if not cont:
        return ''
    soup = BeautifulSoup(cont, 'html.parser')
    url = ''
    if 'comment_loading' in cont:
        url = soup.find(attrs={'node-type': 'comment_loading'}).get('action-data')

    if 'click_more_comment' in cont:
        url = soup.find(attrs={'action-type': 'click_more_comment'}).get('action-data')
    return url


@parse_decorator([])
def get_comment_list(html, wb_id):
    """
    获取评论列表
    :param html: 
    :param wb_id: 
    :return: 
    """
    cont = get_html_cont(html)
    if not cont:
        return list()

    soup = BeautifulSoup(cont, 'html5lib')
    comment_list = list()
    comments = soup.find(attrs={'node-type': 'comment_list'}).find_all(attrs={'class': 'list_li S_line1 clearfix'})

    for comment in comments:
        wb_comment = WeiboComment()
        try:
            cont = []
            first_author=True
            first_colon=True
            for content in comment.find(attrs={'class': 'WB_text'}).contents:
                if not content:
                    continue
                if content.name =='a':
                    if first_author:
                        first_author=False
                        continue
                    else:
                        if content.text:
                            cont.append(content.text)
                    
                elif content.name=='img':
                    img_title = content.get('title', '')
                    if img_title=='':
                        img_title = content.get('alt', '')
                    if img_title=='':
                        img_src = content.get('src','')
                        img_src = img_src.split('/')[-1].split('.',1)[0]
                        try:
                            img_title = parse_emoji.softband_to_utf8(img_src)
                        except Exception as e:
                            parser.error('解析表情失败，具体信息是{},{}'.format(e, comment))
                            img_title = ''
                    cont.append(img_title)

                else:
                    if first_colon:
                        if content.find('：')==0:
                            cont.append(content.replace('：','',1))
                            first_colon=False
                    else:            
                        cont.append(content)

            wb_comment.comment_cont = ''.join(cont)
            wb_comment.comment_screen_name =comment.find(attrs={'class': 'WB_text'}).find('a').text
            
            wb_comment.comment_id = comment['comment_id']
            # TODO 将wb_comment.user_id加入待爬队列（seed_ids）
            wb_comment.user_id = comment.find(attrs={'class': 'WB_text'}).find('a').get('usercard')[3:]
            # todo 日期格式化
            wb_comment.create_time = comment.find(attrs={'class': 'WB_from S_txt2'}).text
            wb_comment.weibo_id = wb_id
        except Exception as e:
            parser.error('解析评论失败，具体信息是{}'.format(e))
        else:
            comment_list.append(wb_comment)
    return comment_list