from sqlalchemy.exc import IntegrityError as SI
from pymysql.err import IntegrityError as PI
from sqlalchemy.exc import InvalidRequestError

from .models import User
from .basic_db import db_session
from decorators import db_commit_decorator


@db_commit_decorator
def save_users(users):
    try:
        db_session.add_all(users)
        db_session.commit()
    except (SI, PI, InvalidRequestError):
        for user in users:
            save_user(user)


@db_commit_decorator
def save_user(user):
    db_session.add(user)
    db_session.commit()


@db_commit_decorator
def get_user_by_uid(uid):
    return db_session.query(User).filter(User.uid == uid).first()
