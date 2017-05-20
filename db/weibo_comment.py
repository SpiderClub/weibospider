# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboComment
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def save_comments(comment_list):
    for comment in comment_list:
        r = get_comment_by_id(comment.comment_id)
        if not r:
            save_comment(comment)
    db_session.commit()


@db_commit_decorator
def save_comment(comment):
    db_session.add(comment)
    db_session.commit()


def get_comment_by_id(cid):
    return db_session.query(WeiboComment).filter(WeiboComment.comment_id == cid).first()
