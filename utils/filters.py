from bs4 import BeautifulSoup


def url_filter(url):
    if url.lower().startswith('//'):
        return 'http:{}'.format(url)
    elif url.lower().startswith('/'):
        return 'http://weibo.com{}'.format(url)
    else:
        return url


def text_filter(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.text.strip()


__all__ = ['url_filter', 'text_filter']