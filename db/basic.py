import os

from sqlalchemy import (
    create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import db_args


__all__ = ['eng', 'Base', 'db_session', 'metadata']


def get_engine():
    password = os.getenv('DB_PASS', db_args['password'])
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        db_args['db_type'], db_args['user'], password, db_args['host'],
        db_args['port'], db_args['db_name'])
    engine = create_engine(connect_str, encoding='utf-8', pool_recycle=3600)
    return engine


eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
# todo 以别的方式管理session
db_session = Session()
metadata = MetaData(get_engine())

