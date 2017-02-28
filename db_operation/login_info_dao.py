# -*-coding:utf-8 -*-
# 操作登陆信息
from db_operation import db_connect


def get_login_info():
    con = db_connect.get_con()
    sql = ('SELECT * FROM '
           '(SELECT * FROM sina_login_infodangbantest order by dbms_random.value) '
           'WHERE rownum =1')
    r = db_connect.db_queryone(con, sql)
    db_connect.db_close(con)
    login_name = r[2]
    pass_word = r[3]
    return login_name, pass_word
