# coding:utf-8
from db.basic_db import db_session
from db.models import User
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def save_users(users):
    db_session.add_all(users)
    db_session.commit()


@db_commit_decorator
def save_user(user):
    db_session.add(user)
    db_session.commit()


def get_user_by_uid(uid):
    return db_session.query(User).filter(User.uid == uid).first()
