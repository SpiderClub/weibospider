# import os
#
# import pytest
#
# from login import (
#     get_session, get_cookies)
#
#
# @pytest.fixture(scope='session', autouse=True)
# def session():
#     login_account = os.getenv('WEIBO_ACCOUNT')
#     login_pass = os.getenv('WEIBO_PASS')
#     s = get_session(login_account, login_pass)
#     assert s is not None
#     return s
#
#
# @pytest.fixture(scope='session', autouse=True)
# def cookies():
#     return get_cookies()