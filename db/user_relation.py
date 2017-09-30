from .basic_db import db_session
from decorators import db_commit_decorator


@db_commit_decorator
def save_relations(relations):
    """
    :param relations: add all user relations
    :return: None
    """
    db_session.add_all(relations)
    db_session.commit()

