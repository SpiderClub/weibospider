# -*-coding:utf-8 -*-
from sqlalchemy import text
from db.basic_db import db_session
from db.models import LoginInfo


def get_login_info():
    rs = db_session.query(LoginInfo.name, LoginInfo.password, LoginInfo.enable).filter(text('enable=1')).all()
    print(rs)
    return rs


def freeze_account(name):
    account = db_session.query(LoginInfo).filter(LoginInfo.name == name).first()
    account.enable = 0
    db_session.commit()