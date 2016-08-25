import redis, requests, json, time
from gl import headers
from do_login import login_info
from requests.exceptions import SSLError as rsle
from requests.packages.urllib3.exceptions import SSLError as rpuese
from ssl import SSLEOFError as sse


def store_cookie():
    cookie_dict = login_info.get_session()['cookie']
    r = redis.Redis(host='localhost', port=6379, db=0)
    cookiestr = json.dumps(cookie_dict)
    print(cookiestr)
    r.set('userinfo_cookie', cookiestr)


def get_cookie():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.get('userinfo_cookie').decode('utf-8')


def get_session(q):
    while True:
        try:
            session = login_info.get_session()['session']
            if session is None:
                # todo: 邮件通知
                time.sleep(60*5)
                session = login_info.get_session()['session']
        except (sse, rsle, rpuese):
            # 预防因为网络问题导致的登陆不成功
            print('本次登陆出现问题')
            time.sleep(60)
            session = login_info.get_session()['session']
        finally:
            q.put(session)
            # session24小时过期
            time.sleep(10*60*60)


if __name__ == '__main__':
    # store_cookie()
    # time.sleep(10)
    cookie = json.loads(get_cookie())
    #cookies = '{"ALC": "ac%3D0%26bt%3D1472132507%26cv%3D5.0%26et%3D1503668507%26scf%3D%26uid%3D3311212405%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Dd8baaf4706f5ab9d7d1f2ae97344dc36", "tgc": "TGT-MzMxMTIxMjQwNQ==-1472132507-xd-21F2645454A9D70F0E3A6073CB89F777", "sso_info": "v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLOMs4SxjKOEso2DgLWJp5WpmYO0s4yzhLGMo4SyjYOAtQ==", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFymH1jaym3aTyWHHETPdbq5NHD95Q0e02peo2ESh5fWs4DqcjTi--fiKnEi-zEe0et", "SUB": "_2A256uoXLDeTxGeVN6lMT8SzIyzmIHXVZsfADrDV_PUNbm9AKLXbZkW99lI6ISfo8n8ZNyOKTRCUKKy_w_g..", "LT": "1472132507", "ALF": "1503668507", "YF-Ugrow-G0": "b02489d329584fca03ad6347fc915997"}'
    content = requests.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more', headers=headers, cookies=cookie).text
    print(content)

