from bs4 import BeautifulSoup


def is_404(html):
    soup = BeautifulSoup(html, 'html.parser')
    return True if soup.title.text == '404错误' or html == '' else False


def is_403(html):
    soup = BeautifulSoup(html, 'html.parser')
    return True if '访问受限' in soup.title.text else False
