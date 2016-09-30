from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from orm.db_connect import get_dbsession, session_close
Base = declarative_base()