from sqlalchemy.exc import IntegrityError as SI
from pymysql.err import IntegrityError as PI
from sqlalchemy.exc import InvalidRequestError

from .basic_db import db_session
from .models import WeiboComment
from decorators import db_commit_decorator


@db_commit_decorator
def save_comments(comments):
    try:
        db_session.add_all(comments)
        db_session.commit()
    except (SI, PI, InvalidRequestError):
        for comment in comments:
            save_comment(comment)


@db_commit_decorator
def save_comment(comment):
    db_session.add(comment)
    db_session.commit()


def get_comment_by_id(cid):
    return db_session.query(WeiboComment).filter(WeiboComment.comment_id == cid).first()
