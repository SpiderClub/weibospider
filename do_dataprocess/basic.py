from bs4 import BeautifulSoup


def is_404(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 前一种情况是处理直接用js实现重定向的页面
    try:
        if "http://weibo.com/sorry?pagenotfound" in html or soup.title.text == '404错误' or html == '':
            return True
        # 处理转发微博的情况
        elif '此微博已被作者删除' in html:
            return True
        else:
            return False
    except AttributeError:
        return True


def is_403(html):
    soup = BeautifulSoup(html, 'html.parser')
    return True if '访问受限' in soup.title.text else False

if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/2.html', 'rb') as f:
        source = f.read().decode('utf-8')
    print(is_404(source))