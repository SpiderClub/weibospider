import os
import time

import pytest

from decorators import timeout
from utils import (
    send_email, url_filter, text_filter)


EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')


@pytest.mark.parametrize(
    'sleep_time, time_out, expect', [(1, 2, 1), (3, 2, '')], ids=('not_time_out', 'time_out')
)
def test_kill_thread_when_timeout(sleep_time, time_out, expect):
    @timeout(time_out)
    def thread_sleep(n):
        time.sleep(n)
        return n

    rs = thread_sleep(sleep_time)
    assert rs == expect


@pytest.mark.parametrize(
    'email_from, email_pass, email_to, expect', [(
            EMAIL_FROM, EMAIL_PASS, EMAIL_TO, {}), (EMAIL_FROM, '123456', EMAIL_TO, None)]
)
def test_send_email(email_from, email_pass, email_to, expect):
    rs = send_email(email_from, email_pass, email_to)
    assert isinstance(rs, type(expect))


@pytest.mark.parametrize(
    'url, expect', [
        ('//wx2.sinaimg.cn/thumb150/006UVNiNgy1fk6b8ooq4rj30ku0qsww5.jpg', 'http://wx2.sinaimg.cn/thumb150/006UVNiNgy'
                                                                           '1fk6b8ooq4rj30ku0qsww5.jpg'),
        ('//gslb.miaopai.com/stream/LWuG0Ng0AyTCYkzSzt9l0fh6usQP2mSqH~i9rQ__.mp4',
         'http://gslb.miaopai.com/stream/LWuG0Ng0AyTCYkzSzt9l0fh6usQP2mSqH~i9rQ__.mp4'),
        ('/p/1002061402977920/service', 'http://weibo.com/p/1002061402977920/service'),
        ('http://company.verified.weibo.com/bluev/verify/index', 'http://company.verified.weibo.com/bluev/verify/index')
    ]
)
def test_url_filter(url, expect):
    assert url_filter(url) == expect


@pytest.mark.parametrize(
    'text, expect', [
        ('hello,every one', 'hello,every one'),
        ('  hello,every one', 'hello,every one'),
        ('hello,every one  ', 'hello,every one'),
        ('    hello,every one  ', 'hello,every one')
    ]
)
def test_text_filter(text, expect):
    assert text_filter(text) == expect
