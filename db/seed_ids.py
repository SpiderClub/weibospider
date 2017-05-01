from sqlalchemy import text
from db.basic_db import db_session
from db.models import SeedIds


def get_seed_ids():
    return db_session.query(SeedIds.uid).filter(text('is_crawled=0')).all()


def set_seed_crawled(uid):
    seed = db_session.query(SeedIds).filter(SeedIds.uid == uid).first()
    seed.is_crawled = 1
    db_session.commit()