# -*-coding:utf-8 -*-
from db import db_connect


def get_login_info():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = 'select name, password from login_info where enable = 1'

    datas = list()
    with db_connect.db_execute() as conn:
        rs = db_connect.db_queryall(conn, sql)
        for r in rs:
            name = r[0]
            password = r[1]
            datas.append(dict(name=name, password=password))
    return datas