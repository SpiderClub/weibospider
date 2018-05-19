import sys

# to work well inside config module or outsize config module
sys.path.append('..')
sys.path.append('.')

from ..db.tables import *
from ..db.basic import metadata


def create_all_table():
    metadata.create_all()

