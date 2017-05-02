# -*-coding:utf-8 -*-
from sqlalchemy import Column, INTEGER, String
from db.basic_db import Base


class LoginInfo(Base):
    __tablename__ = 'login_info'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(100))
    password = Column(String(200))
    enable = Column(INTEGER, default=1)


class User(Base):
    __tablename__ = 'wbuser'
    # 这里需要设置默认值，否则空的话可能会存储None，可能会引发未catch的异常
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True)
    name = Column(String(200), default='')
    gender = Column(INTEGER, default=0)
    birthday = Column(String(200), default='')
    location = Column(String(100), default='')
    description = Column(String(500), default='')
    register_time = Column(String(200), default='')
    verify_type = Column(INTEGER, default=0)
    verify_info = Column(String(300), default='')
    follows_num = Column(INTEGER, default=0)
    fans_num = Column(INTEGER, default=0)
    wb_num = Column(INTEGER, default=0)
    level = Column(INTEGER, default=0)
    tags = Column(String(500), default='')
    work_info = Column(String(500), default='')
    contact_info = Column(String(300), default='')
    education_info = Column(String(300), default='')
    head_img = Column(String(500), default='')


class SeedIds(Base):
    __tablename__ = 'seed_ids'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True)
    is_crawled = Column(INTEGER, default=0)
    other_crawled = Column(INTEGER, default=0)