# -*-coding:utf-8 -*-
from db import basic


def get_login_info():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = 'select name, password from login_info where enable = 1'

    datas = list()
    with basic.db_execute() as conn:
        rs = basic.db_queryall(conn, sql)
        for r in rs:
            name = r[0]
            password = r[1]
            datas.append(dict(name=name, password=password))
    return datas


def freeze_account(name):
    sql = 'update weibo_login_info set enable = 0 where name = :name'
    args = dict(name=name)
    with basic.db_execute() as conn:
        basic.db_dml_parms(conn, sql, args)