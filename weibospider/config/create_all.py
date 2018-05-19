import sys

# to work well inside config module or outsize config module
sys.path.append('..')
sys.path.append('.')

from ..db.tables import *
from ..db.basic import (
    metadata, create_db)


def create_all():
    create_db()
    metadata.create_all()

