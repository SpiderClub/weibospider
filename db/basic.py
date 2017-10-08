import os

from sqlalchemy import (
    create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import get_db_args


def get_engine():
    args = get_db_args()
    password = os.getenv('DB_PASS', args['password'])
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(args['db_type'], args['user'], password,
                                                             args['host'], args['port'], args['db_name'])
    engine = create_engine(connect_str, encoding='utf-8')
    return engine


eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = Session()
metadata = MetaData(get_engine())


__all__ = ['eng', 'Base', 'db_session', 'metadata']
