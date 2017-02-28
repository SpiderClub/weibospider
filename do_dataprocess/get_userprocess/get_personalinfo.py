# -*-coding:utf-8 -*-
# 个人用户个人资料页
from bs4 import BeautifulSoup
from do_dataprocess.get_userprocess import get_publicinfo
from weibo_decorator.decorators import parse_decorator
from weibo_entities.user import User


@parse_decorator(0)
def get_friends(html):
    """
    :param html:
    :return: 返回关注数
    """
    cont = get_publicinfo.get_left(html)
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
    cont = get_publicinfo.get_left(html)
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
    cont = get_publicinfo.get_left(html)
    if cont == '':
        return 0
    soup = BeautifulSoup(cont, 'html.parser')
    try:
        return int(soup.find_all('strong')[2].get_text())
    except Exception:
        return 0


@parse_decorator(5)
# todo 补充所有信息
def get_detail(html):
    user = User()
    cont = get_publicinfo.get_right(html)
    if cont == '':
        return user
    soup = BeautifulSoup(cont, 'html.parser')
    basic_modules = soup.find_all(attrs={'class': 'WB_cardwrap S_bg2'})
    basic_info = soup.find_all(attrs={'class': 'li_1 clearfix'})
    for each_module in basic_modules:
        try:
            basic_str = each_module.find(attrs={'class': 'main_title W_fb W_f14'}).get_text()
            if '基本信息' in basic_str:
                for each in basic_info:
                    each_str = each.get_text()
                    if '昵称' in each_str:
                        nickname = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_screen_name = nickname
                    elif '所在地' in each_str:
                        location = each.find(attrs={'class': 'pt_detail'}).get_text()
                        if ' ' in location:
                            province = location.split(' ')[0]
                            city = location.split(' ')[1]
                            user.su_province = province
                            user.su_city = city
                        else:
                            user.su_province = location
                            user.su_city = ''
                    elif '性别' in each_str:
                        gender = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_gender = gender
                    elif '性取向' in each_str:
                        gender_prefer = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_gender_prefer = gender_prefer
                    # elif '感情状况' in each_str:
                    #     loving = each.find(attrs={'class': 'pt_detail'}).get_text()
                    elif '生日' in each_str:
                        birthday = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_birthday = birthday
                    elif '血型' in each_str:
                        blood_type = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_blood_type = blood_type
                    elif '博客' in each_str:
                        blog_url = each.find('a').get_text()
                        user.su_blog_url = blog_url
                    elif '简介' in each_str:
                        description = each.find(attrs={'class': 'pt_detail'}).get_text()
                        user.su_description = description.encode('gbk', 'ignore').decode('gbk')
                    elif '注册时间' in each_str:
                        register_time = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\t', '').replace('\r\n','')
                        user.su_register_time = register_time
                    elif '个性域名' in each_str:
                        personal_domain = each.find('a').get_text()
                        user.su_domain_name = personal_domain

            if '标签信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                for each in basic_info:
                    if '标签' in each.get_text():
                        tags = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\t', '').replace('\n\n\n', '')\
                            .strip().replace('\r\n', ';')
                        user.su_owntag_info = tags

            if '教育信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                for each in basic_info:
                    if '大学' in each.get_text():
                        school_info = each.find(attrs={'class': 'pt_detail'}).get_text().replace('\r\n', ',')\
                            .replace('\t', '').replace('\n', ';').lstrip(';').rstrip(';')
                        user.su_educate_info = school_info

            if '工作信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                jobs_info = []
                for each in basic_info:
                    if '公司' in each.get_text():
                        jobs = each.find_all(attrs={'class': 'pt_detail'})
                        for job in jobs:
                            jobs_info.append(job.get_text().replace('\r\n', '').replace('\t', '').replace('\n', ''))
                all_job = ';'.join(jobs_info)
                user.su_work_info = all_job

            if '联系信息' in basic_str:
                basic_info = each_module.find_all(attrs={'class': 'li_1 clearfix'})
                contact_info = []
                for each in basic_info:
                    if 'QQ' in each.get_text():
                        contact_info.append('qq:'+each.find(attrs={'class': 'pt_detail'}).get_text().replace('\n', ''))
                    if '邮箱' in each.get_text():
                        contact_info.append('email:'+each.find(attrs={'class': 'pt_detail'}).get_text())
                    if 'MSN' in each.get_text():
                        contact_info.append('msn:'+each.find(attrs={'class': 'pt_detail'}).get_text())
                contact_str = ';'.join(contact_info)
                user.su_contact_info = contact_str
        except Exception as why:
            print('解析出错，具体原因为{why}'.format(why=why))
        finally:
            return user


if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/luce.html', 'rb') as f:
        source = f.read().decode('utf-8')
    u = get_detail(source)
    print(u.description.encode('utf-8').decode('utf-8'))
