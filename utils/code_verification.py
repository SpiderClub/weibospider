import json
import time

import requests
from hashlib import md5

from logger import other


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def code_verificate(name, passwd, file_name, code_type=1005, app_id=3510, app_key='7281f8452aa559cdad6673684aa8f575',
                    time_out=60):
    chaojiying = Chaojiying_Client('超级鹰用户名', '密码', '96001')  # 替换用户名和密码即可。
    im = open(file_name, 'rb').read()
    api_cjy_result = chaojiying.PostPic(im, 1902)
    rs = api_cjy_result['pic_str']
    err_no = api_cjy_result['err_no']
    cid = api_cjy_result['pic_id']

    return rs, chaojiying, cid, err_no
