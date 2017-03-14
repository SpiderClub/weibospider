# -*-coding:utf-8 -*-
# 获取扩散信息
import requests
import re
import json
import os
import execjs
import headers
from logger.log import other
from config.get_config import get_weibo_args


def get_runntime(path):
    """
    :param path: 加密js的路径,注意js中不要使用中文！估计是pyexecjs处理中文还有一些问题
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    phantom = execjs.get('PhantomJS')  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    with open(path, 'r') as f:
        source = f.read()
    return phantom.compile(source)


# 获取经base64编码的用户名
def get_encodename(name, runntime):
    return runntime.call('get_name', name)


# 获取加密后的密码
def get_pass(password, pre_obj, runntime):
    """
    :param password: 登陆密码
    :param pre_obj: 返回的预登陆信息
    :param runntime: 运行时环境
    :return: 加密后的密码
    """
    nonce = pre_obj['nonce']
    pubkey = pre_obj['pubkey']
    servertime = pre_obj['servertime']
    return runntime.call('get_pass', password, nonce, servertime, pubkey)


# 获取预登陆返回的信息
def get_prelogin_info(prelogin_url, session):
    json_pattern = r'.*?\((.*)\)'
    repose_str = session.get(prelogin_url).text
    m = re.match(json_pattern, repose_str)
    return json.loads(m.group(1))


# 使用post提交加密后的所有数据,并且获得下一次需要get请求的地址
def get_redirect(data, post_url, session):
    """
    :param data: 需要提交的数据，可以通过抓包来确定部分不变的
    :param post_url: post地址
    :param session:
    :return: 服务器返回的下一次需要请求的url
    """
    header = {
        'Referer': 'http://weibo.com/',
        'Host': 'login.sina.com.cn'
    }
    headers.headers.update(header)
    logining_page = session.post(post_url, data=data, headers=headers.headers)
    post_cookie = logining_page.cookies
    login_loop = logining_page.content.decode("GBK")
    if '正在登录' in login_loop:
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        return re.findall(pa, login_loop)[0], post_cookie
    else:
        return '', post_cookie


# 获取成功登陆返回的信息,包括用户id等重要信息,返回登陆session
def get_session():
    name_password = get_weibo_args()
    session = requests.Session()
    js_path = os.path.join(os.getcwd(), 'wblogin/sinalogin.js')
    runntime = get_runntime(js_path)

    su = get_encodename(name_password['name'], runntime)
    post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' \
                   'su=' + su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
    pre_obj = get_prelogin_info(prelogin_url, session)
    sp = get_pass(name_password['password'], pre_obj, runntime)

    # 提交的数据可以根据抓包获得
    data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': pre_obj['nonce'],
        'pagerefer': "",
        'prelt': 67,
        'pwencode': 'rsa2',
        "returntype": "META",
        'rsakv': pre_obj['rsakv'],
        'savestate': '7',
        'servertime': pre_obj['servertime'],
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': su,
        'useticket': '1',
        'vsnf': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
    }

    rs_datas = get_redirect(data, post_url, session)

    url = rs_datas[0]
    if url != '':
        post_cookies = rs_datas[1]
        rs_cont = session.get(url)
        cookies = requests.utils.dict_from_cookiejar(rs_cont.cookies)
        last_cookies = requests.utils.add_dict_to_cookiejar(post_cookies, cookies)
        login_info = rs_cont.text
        u_pattern = r'"uniqueid":"(.*)",'
        m = re.search(u_pattern, login_info)
        if m:
            if m.group(1):
                other.info('本次登陆账号为:{name}'.format(name=name_password['name']))
                return {'session': session, 'cookie': dict(last_cookies)}
            else:
                other.error('本次账号{name}登陆失败'.format(name=name_password['name']))
                return None
        else:
            other.error('本次账号{name}登陆失败'.format(name=name_password['name']))
    else:
        other.error('本次账号{name}登陆失败'.format(name=name_password['name']))
        return None
