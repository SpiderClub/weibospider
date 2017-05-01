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
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uid = Column(INTEGER, unique=True)
    name = Column(String(200))
    gender = Column(INTEGER)
    birthday = Column(String(200))
    location = Column(String(100))
    description = Column(String(500))
    register_time = Column(String(200))
    is_verify = Column(INTEGER)
    verify_type = Column(INTEGER)
    verify_info = Column(String(300))
    follows_num = Column(INTEGER)
    fans_num = Column(INTEGER)
    wb_num = Column(INTEGER)
    level = Column(INTEGER)
    tags = Column(String(500))
    work_info = Column(String(500))
    contact_info = Column(String(300))
    education_info = Column(String(300))
    head_img = Column(String(500))
    # TODO 先不做__init__操作，看看默认值是否有效
    # def __init__(self):
    #     self.name = ''
    #     self.location = ''
    #     self.description = ''
    #     self.head_img = ''
    #     self.gender = 0
    #     self.level = 0
    #     self.followers_num = 0
    #     self.fans_num = 0
    #     self.wb_num = 0
    #     self.birthday = ''
    #     self.contact_info = ''
    #     self.work_info = ''
    #     self.education_info = ''
    #     self.tags = ''
    #     self.register_time = ''
    #     self.is_verify = 0
    #     self.verify_type = 0
    #     self.verify_info = ''

    def __str__(self):
        return 'id = {id},name={name}, location={location}, verify_type={vt},verify_info={vi}, description={desc}'.\
            format(id=self.uid, name=self.name, location=self.location, vt=self.verify_type, vi=self.verify_info,
                   desc=self.description)


class SpreadOriginal(object):
    pass