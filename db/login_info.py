# -*-coding:utf-8 -*-
from sqlalchemy import text
from db.basic_db import db_session
from db.models import LoginInfo
from decorators.decorator import db_commit_decorator


def get_login_info():
    return db_session.query(LoginInfo.name, LoginInfo.password, LoginInfo.enable).\
        filter(text('enable=1')).all()


@db_commit_decorator
def freeze_account(name, rs):
    """
    :param name: 账户名
    :param rs: 0表示被封，1表示正常，2表示账号密码不匹配
    :return: 
    """
    account = db_session.query(LoginInfo).filter(LoginInfo.name == name).first()
    account.enable = rs
    db_session.commit()