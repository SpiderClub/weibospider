def url_filter(url):
    if 'http' not in url:
        return 'http:{}'.format(url)
    elif 'sina' or 'weibo' not in url:
        return 'http://weibo.com{}'.format(url)
    else:
        return url