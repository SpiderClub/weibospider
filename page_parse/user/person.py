from bs4 import BeautifulSoup

from ..user import public
from decorators import parse_decorator
from db.models import User


@parse_decorator(0)
def get_friends(html):
    """
    :param html:
    :return: 返回关注数
    """
    cont = public.get_left(html)
    if cont == '':
        return 0
    soup = BeautifulSoup(cont, 'html.parser')
    try:
        return int(soup.find_all('strong')[0].get_text())
    except Exception:
        return 0


@parse_decorator(0)
def get_fans(html):
    """
    :param html:
    :return: 返回粉丝数
    """
    cont = public.get_left(html)
    if cont == '':
        return 0
    soup = BeautifulSoup(cont, 'html.parser')
    try:
        return int(soup.find_all('strong')[1].get_text())
    except Exception:
        return 0


@parse_decorator(0)
def get_status(html):
    """
    :param html:
    :return: 返回微博总数
    """
    cont = public.get_left(html)
    if cont == '':
        return 0
    soup = BeautifulSoup(cont, 'html.parser')
    try:
        return int(soup.find_all('strong')[2].get_text())
    except Exception:
        return 0


@parse_decorator(None)
# todo 补充所有信息， 优化代码
def get_detail(html, uid):
    user = User(uid)
    cont = public.get_right(html)
    if cont == '':
        return None
    soup = BeautifulSoup(cont, 'html.parser')
    basic_modules = soup.find_all(attrs={'class': 'WB_cardwrap S_bg2'})
    basic_info = soup.find_all(attrs={'class': 'li_1 clearfix'})
    for each_module in basic_modules:
        try:
            basic_str = each_module.find(attrs={'class': 'main_title W_fb W_f14'}).get_text()
            if '基本信息' in basic_str:
                for each in basic_info:
                    each_str = each.get_text()
                    if '昵称：' in each_str:
                        user.name = each.find(attrs={'class': 'pt_detail'}).get_text()
                    elif '所在地：' in each_str:
                        user.location = each.find(attrs={'class': 'pt_detail'}).get_text()
                    elif '性别：' in each_str:
                        gender = each.find(attrs={'class': 'pt_detail'}).get_text()
                        if gender == '男':
                            user.gender = 1
                        elif gender == '女':
                            user.gender = 2
                        else:
                            user.gender = 0
                    elif '生日：' in each_str:
                        user.birthday = each.find(attrs={'class': 'pt_detail'}).get_text()
                    elif '简介：' in each_str:
                        description = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.description = description.encode('gbk', 'ignore').decode('gbk')
                    elif '注册时间：' in each_str:
                        user.register_time = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\t', '').replace(
                            '\r\n', '')

            if '标签信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                for each in basic_info:
                    if '标签：' in each.get_text():
                        user.tags = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\t', '').replace(
                            '\n\n\n', '') .strip().replace('\r\n', ';')

            if '教育信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                for each in basic_info:
                    if '大学：' in each.get_text():
                        user.education_info = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\r\n', ',') \
                            .replace('\t', '').replace('\n', ';').lstrip(';').rstrip(';')

            if '工作信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                jobs_info = []
                for each in basic_info:
                    if '公司：' in each.get_text():
                        jobs = each.find_all(attrs={'class': 'pt_detail'})
                        for job in jobs:
                            jobs_info.append(job.get_text().replace('\r\n', '').replace('\t', '').replace('\n', ''))
                user.work_info = ';'.join(jobs_info)

            if '联系信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                contact_info = []
                for each in basic_info:
                    if 'QQ：' in each.get_text():
                        contact_info.append(
                            'qq:' + each.find(attrs={'class': 'pt_detail'}).get_text().replace('\n', ''))
                    if '邮箱：' in each.get_text():
                        contact_info.append('email:' + each.find(attrs={'class': 'pt_detail'}).get_text())
                    if 'MSN：' in each.get_text():
                        contact_info.append('msn:' + each.find(attrs={'class': 'pt_detail'}).get_text())
                user.contact_info = ';'.join(contact_info)
        except Exception as why:
            print('解析出错，具体原因为{why}'.format(why=why))

    return user
