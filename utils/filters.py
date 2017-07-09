def url_filter(url):
    if 'sina' or 'weibo' not in url:
        return 'http://weibo.com{}'.format(url)
    elif 'http:' not in url:
        return 'http:{}'.format(url)
    else:
        return url