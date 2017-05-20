#!/usr/bin/env python
#-*- coding=utf-8 -*-

#from sqlalchemy import MetaData

from db.basic_db import metadata
from db.tables import *

def create_all_table():
    metadata.create_all()

if __name__ == "__main__":
    create_all_table()
