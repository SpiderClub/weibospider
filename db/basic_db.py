# -*-coding:utf-8 -*-
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.conf import get_db_args
from contextlib import contextmanager
from logger.log import storage


def get_engine():
    args = get_db_args()
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(args['db_type'], args['user'], args['password'],
                                                             args['host'], args['port'], args['db_name'])
    engine = create_engine(connect_str, encoding="utf-8")
    return engine


def db_close(con):
    con.close()


def db_queryall(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


def db_queryone(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result


def db_queryone_params(con, sql, params):
    cursor = con.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    return result


def db_queryall_params(con, sql, params):
    cursor = con.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    return result


def db_dml(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()


def db_dml_parms(con, sql, parms):
    cursor = con.cursor()
    cursor.execute(sql, parms)
    con.commit()
    cursor.close()


def db_dml_many(con, sql, params_list):
    cursor = con.cursor()
    cursor.executemany(sql, params_list)
    con.commit()
    cursor.close()


@contextmanager
def db_execute():
    con = None

    try:
        con = get_engine()
    except Exception as e:
        storage.error('连接数据库错误，具体信息是{e}'.format(e=e))

    try:
        yield con
    except Exception as e:
        storage.error('操作数据库出错，具体信息是{e},\n堆栈信息是{detail}'.format(e=e, detail=repr(traceback.format_stack())))


eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = Session()


__all__ = ['eng', 'Base', 'db_session']