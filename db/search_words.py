# -*-coding:utf-8 -*-
from sqlalchemy import text
from db.basic_db import db_session
from db.models import KeyWords
from decorators.decorator import db_commit_decorator


def get_search_keywords():
    return db_session.query(KeyWords.keyword, KeyWords.id).filter(text('enable=1')).all()


@db_commit_decorator
def set_useless_keyword(keyword):
    search_word = db_session.query(KeyWords).filter(KeyWords.keyword == keyword).first()
    search_word.enable = 0
    db_session.commit()
