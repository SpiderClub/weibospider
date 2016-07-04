import requests
from gl import headers
from get_cookie import get_cookie
from do_login import login_info


if __name__ == '__main__':

    cookie_dict = login_info.get_session()['cookie']
    print(cookie_dict)
    print(type(cookie_dict))
    cookie = [item["name"] + "=" + item["value"] for item in cookie_dict]
    cookiestr = '; '.join(item for item in cookie)
    print(cookiestr)
    content = requests.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more', cookies=cookiestr, headers=headers).text
    print(content)