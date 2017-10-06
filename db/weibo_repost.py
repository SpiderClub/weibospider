from sqlalchemy.exc import IntegrityError as SI
from pymysql.err import IntegrityError as PI
from sqlalchemy.exc import InvalidRequestError

from .basic_db import db_session
from .models import WeiboRepost
from decorators import db_commit_decorator


def get_repost_by_rid(rid):
    return db_session.query(WeiboRepost).filter(WeiboRepost.weibo_id == rid).first()


@db_commit_decorator
def save_reposts(reposts):
    try:
        db_session.add_all(reposts)
        db_session.commit()
    except (SI, PI, InvalidRequestError):
        for repost in reposts:
            save_repost(repost)


@db_commit_decorator
def save_repost(repost):
    db_session.add(repost)
    db_session.commit()