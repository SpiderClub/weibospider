# -*-coding:utf-8 -*-
import cx_Oracle
import gl


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
#
# if __name__ == '__main__':
#     log_path = os.path.join(os.getcwd(), 'repost_info.log')
#     logging.basicConfig(filename=log_path, level=logging.DEBUG, format='[%(asctime)s %(levelname)s] %(message)s',
#                         datefmt='%Y%m%d %H:%M:%S')
#     logging.debug('本次抓取时间为:{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
