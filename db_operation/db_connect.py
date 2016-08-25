# -*-coding:utf-8 -*-
import cx_Oracle, redis,gl


def get_con():
    dsn = cx_Oracle.makedsn(gl.host, gl.port, gl.dbname)
    conn = cx_Oracle.connect(gl.user, gl.password, dsn)
    return conn


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


def get_redis_con(host, port, db):
    return redis.Redis(host=host, port=port, db=db)

