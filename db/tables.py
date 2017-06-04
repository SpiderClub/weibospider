# -*-coding:utf-8 -*-
from sqlalchemy import Table, Column, INTEGER, String
from db.basic_db import metadata

# 登陆帐号表 login_info
login_info = Table("login_info", metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("name", String(100), unique=True),
                   Column("password", String(200)),
                   Column("enable", INTEGER, default=1, server_default='1'),
                   )

# 用户表 wbuser
wbuser = Table("wbuser", metadata,
               # 这里需要设置默认值，否则空的话可能会存储None，可能会引发未catch的异常
               Column("id", INTEGER, primary_key=True, autoincrement=True),
               Column("uid", String(20), unique=True),
               Column("name", String(200), default='', server_default=''),
               Column("gender", INTEGER, default=0, server_default='0'),
               Column("birthday", String(200), default='', server_default=''),
               Column("location", String(100), default='', server_default=''),
               Column("description", String(500), default='', server_default=''),
               Column("register_time", String(200), default='', server_default=''),
               Column("verify_type", INTEGER, default=0, server_default='0'),
               Column("verify_info", String(300), default='', server_default=''),
               Column("follows_num", INTEGER, default=0, server_default='0'),
               Column("fans_num", INTEGER, default=0, server_default='0'),
               Column("wb_num", INTEGER, default=0, server_default='0'),
               Column("level", INTEGER, default=0, server_default='0'),
               Column("tags", String(500), default='', server_default=''),
               Column("work_info", String(500), default='', server_default=''),
               Column("contact_info", String(300), default='', server_default=''),
               Column("education_info", String(300), default='', server_default=''),
               Column("head_img", String(500), default='', server_default=''),
               )

# 种子用户表 seed_ids
seed_ids = Table('seed_ids', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True),
                 Column("uid", String(20), unique=True),
                 Column("is_crawled", INTEGER, default=0, server_default='0'),
                 Column("other_crawled", INTEGER, default=0, server_default='0'),
                 Column("home_crawled", INTEGER, default=0, server_default='0'),
                 )

# 关键词搜索表 keywords
keywords = Table('keywords', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True),
                 Column("keyword", String(200), unique=True),
                 Column("enable", INTEGER, default=1, server_default='1'),
                 )

# 微博信息表 weibo_data
weibo_data = Table('weibo_data', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("weibo_id", String(200), unique=True),
                   Column("weibo_cont", String(6000), default='', server_default=''),
                   Column("repost_num", INTEGER, default=0, server_default='0'),
                   Column("comment_num", INTEGER, default=0, server_default='0'),
                   Column("praise_num", INTEGER, default=0, server_default='0'),
                   Column("uid", String(20)),
                   Column("is_origin", INTEGER, default=1, server_default='1'),
                   Column("device", String(200), default='', server_default=''),
                   Column("weibo_url", String(300)),
                   Column("create_time", String(200)),
                   Column("comment_crawled", INTEGER, default=0, server_default='0'),
                   Column("repost_crawled", INTEGER, default=0, server_default='0'),
                   )

# 微博信息关键词联系表 keywords_wbdata
keywords_wbdata = Table('keywords_wbdata', metadata,
                        Column("id", INTEGER, primary_key=True, autoincrement=True),
                        Column("keyword_id", INTEGER),
                        Column("wb_id", String(200)),
                        )

# 微博评论表
weibo_comment = Table('weibo_comment', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True),
                      Column("comment_id", String(50)),
                      Column("comment_cont", String(5000)),
                      Column("weibo_id", String(200)),
                      Column("user_id", String(20)),
                      Column("create_time", String(200)),
                      )

# 微博转发评论
weibo_repost = Table("weibo_repost", metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                     Column("user_id", String(20)),
                     Column("user_name", String(200)),
                     Column("weibo_id", String(200), unique=True),
                     Column("parent_user_id", String(20)),
                     Column("repost_time", String(200)),
                     Column("repost_cont", String(20), default='', server_default=''),
                     Column("weibo_url", String(200)),
                     Column("parent_user_name", String(200)),
                     Column("root_weibo_id", String(200)),
                     )

__all__ = ['login_info', 'wbuser', 'seed_ids', 'keywords', 'weibo_data', 'keywords_wbdata', 'weibo_comment',
           'weibo_repost']