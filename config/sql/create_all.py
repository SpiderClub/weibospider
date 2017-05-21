# -*- coding=utf-8 -*-
from db.tables import *
from db.basic_db import metadata


def create_all_table():
    metadata.create_all()

if __name__ == "__main__":
    create_all_table()
