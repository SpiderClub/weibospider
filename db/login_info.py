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
    :param name: login account
    :param rs: 0 stands for banned，1 stands for normal，2 stands for name or password is invalid
    :return: 
    """
    account = db_session.query(LoginInfo).filter(LoginInfo.name == name).first()
    account.enable = rs
    db_session.commit()