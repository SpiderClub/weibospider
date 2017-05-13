# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboComment
from pymysql.err import IntegrityError
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def save_comments(comment_list):
    try:
        db_session.add_all(comment_list)
    except IntegrityError:
        for data in comment_list:
            r = get_comment_by_id(data.comment_id)
            if r:
                continue
            save_comment(data)
    finally:
        db_session.commit()


@db_commit_decorator
def save_comment(comment):
    db_session.add(comment)
    db_session.commit()


def get_comment_by_id(cid):
    return db_session.query(WeiboComment).filter(WeiboComment.comment_id == cid).first()
