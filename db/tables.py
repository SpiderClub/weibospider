from sqlalchemy import (
    Table, Column, INTEGER, String, Text)

from .basic import metadata

# login table
login_info = Table("login_info", metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("name", String(100), unique=True),
                   Column("password", String(200)),
                   Column("enable", INTEGER, default=1, server_default='1'),
                   )

# weibo user info
wbuser = Table("wbuser", metadata,
               Column("id", INTEGER, primary_key=True, autoincrement=True),
               Column("uid", String(20), unique=True),
               Column("name", String(200), default='', server_default=''),
               Column("gender", INTEGER, default=0, server_default='0'),
               Column("birthday", String(200), default='', server_default=''),
               Column("location", String(100), default='', server_default=''),
               Column("description", String(500), default='', server_default=''),
               Column("register_time", String(200), default='', server_default=''),
               Column("verify_type", INTEGER, default=0, server_default='0'),
               Column("verify_info", String(2500), default='', server_default=''),
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

# seed ids for user crawling
seed_ids = Table('seed_ids', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True),
                 Column("uid", String(20), unique=True),
                 Column("is_crawled", INTEGER, default=0, server_default='0'),
                 Column("other_crawled", INTEGER, default=0, server_default='0'),
                 Column("home_crawled", INTEGER, default=0, server_default='0'),
                 )

# search keywords table
keywords = Table('keywords', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True),
                 Column("keyword", String(200), unique=True),
                 Column("enable", INTEGER, default=1, server_default='1'),
                 )

# weibo info data
weibo_data = Table('weibo_data', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("weibo_id", String(200), unique=True),
                   Column("weibo_cont", Text),
                   Column("weibo_img", String(1000)),
                   Column("weibo_img_path", String(1000), server_default=''),
                   Column("weibo_video", String(1000)),
                   Column("repost_num", INTEGER, default=0, server_default='0'),
                   Column("comment_num", INTEGER, default=0, server_default='0'),
                   Column("praise_num", INTEGER, default=0, server_default='0'),
                   Column("uid", String(20)),
                   Column("is_origin", INTEGER, default=1, server_default='1'),
                   Column("device", String(200), default='', server_default=''),
                   Column("weibo_url", String(300), default='', server_default=''),
                   Column("create_time", String(200)),
                   Column("comment_crawled", INTEGER, default=0, server_default='0'),
                   Column("repost_crawled", INTEGER, default=0, server_default='0'),
                   Column("dialogue_crawled", INTEGER, default=0, server_default='0'),
                   )

# keywords and weibodata relationship
keywords_wbdata = Table('keywords_wbdata', metadata,
                        Column("id", INTEGER, primary_key=True, autoincrement=True),
                        Column("keyword_id", INTEGER),
                        Column("wb_id", String(200)),
                        )

# comment table
weibo_comment = Table('weibo_comment', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True),
                      Column("comment_id", String(50), unique=True),
                      Column("comment_cont", Text),
                      Column("weibo_id", String(200)),
                      Column("user_id", String(20)),
                      Column("create_time", String(200)),
                      )

# repost table
weibo_repost = Table("weibo_repost", metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                     Column("user_id", String(20)),
                     Column("user_name", String(200)),
                     Column("weibo_id", String(200), unique=True),
                     Column("parent_user_id", String(20)),
                     Column("repost_time", String(200)),
                     Column("repost_cont", Text),
                     Column("weibo_url", String(200)),
                     Column("parent_user_name", String(200)),
                     Column("root_weibo_id", String(200)),
                     )

# relations about user and there fans and follows
user_relation = Table("user_relation", metadata,
                      Column('id', INTEGER, primary_key=True, autoincrement=True),
                      Column('user_id', String(20)),
                      Column('follow_or_fans_id', String(20)),
                      Column('type', INTEGER),  # 1 stands for fans, 2 stands for follows
                      )

# dialogue table
weibo_dialogue = Table("weibo_dialogue", metadata,
                       Column("id", INTEGER, primary_key=True, autoincrement=True),
                       Column("dialogue_id", String(50), unique=True),
                       Column("weibo_id", String(200)),
                       Column("dialogue_cont", Text),
                       Column("dialogue_rounds", INTEGER),
                       )

__all__ = ['login_info', 'wbuser', 'seed_ids', 'keywords', 'weibo_data', 'keywords_wbdata', 'weibo_comment',
           'weibo_repost', 'user_relation', 'weibo_dialogue']
