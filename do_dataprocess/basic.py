# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup


def is_404(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 前一种情况是处理直接用js实现重定向的页面
    try:
        if "http://weibo.com/sorry?pagenotfound" in html or soup.title.text == '404错误' or html == '':
            return True
        # 处理转发微博的情况
        elif '抱歉，此微博已被作者删除' in html:
            return True
        else:
            return False
    except AttributeError:
        return True


def is_403(html):
    soup = BeautifulSoup(html, 'html.parser')
    if 'uid' not in html or '访问受限' in soup.title.text:
        return True
    else:
        return False

if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/1.html', 'rb') as f:
        source = f.read().decode('utf-8')
    print(is_403(source))