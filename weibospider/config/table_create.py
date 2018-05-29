import sys
import warnings

# to work well inside config module or outsize config module
sys.path.append('..')
sys.path.append('.')

from ..logger import db_logger
from ..db.tables import *
from ..db.basic import (
    metadata, create_db)


def create_all():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        create_db()
        metadata.create_all()
        db_logger.info('init db successfully!')

