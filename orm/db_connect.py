from orm import *


def get_engine():
    db_type = get_oracle_args()['db_type']
    name = get_oracle_args()['user']
    password = get_oracle_args()['password']
    host = get_oracle_args()['host']
    port = get_oracle_args()['port']
    db = get_oracle_args()['db']
    dsn = db_type + "://" + name + ':' + password + '@' + host + ':' + port + '/' + db
    return create_engine(dsn, encoding='utf-8')


def get_conn():
    engine = get_engine()
    return engine.connect()


def get_dbsession():
    engine = get_engine()
    DBSsession = sessionmaker(bind=engine)
    return DBSsession()


def session_close(session):
    session.close()

if __name__ == '__main__':
    conn = get_conn()
    sql = 'select * from sina_login_infodangban_filter'
    rs = conn.execute(sql)
    for row in rs:
        print(row['id'])

