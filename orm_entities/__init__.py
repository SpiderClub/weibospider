from urllib.parse import urljoin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime,desc
from orm.db_connect import get_dbsession, session_close
from weibo_decorator.decorators import dbtimeout_decorator, save_decorator
from gl import base_url
Base = declarative_base()