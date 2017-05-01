# -*-coding:utf-8 -*-
from db import basic_db


def get_login_info():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = 'select name, password from weibo_login_info where enable = 1'

    datas = list()
    with basic_db.db_execute() as conn:
        rs = basic_db.db_queryall(conn, sql)
        for r in rs:
            name = r[0]
            password = r[1]
            datas.append(dict(name=name, password=password))
    return datas


def set_account_freeze(name):
    sql = 'update weibo_login_info set enable = 0 where name = :name'
    args = dict(name=name)
    with basic_db.db_execute() as conn:
        basic_db.db_dml_parms(conn, sql, args)