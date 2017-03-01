# -*-coding:utf-8 -*-
from contextlib import contextmanager
from db_operation import db_connect
from logger.log import storage


@contextmanager
def db_execute():
    con = None
    try:
        con = db_connect.get_con()
    except Exception as e:
        storage.error('连接数据库错误，具体信息是{e}'.format(e=e))
    try:
        yield con
    except Exception as e:
        storage.error('操作数据库出错，具体信息是{e}'.format(e=e))
    finally:
        if con:
            db_connect.db_close(con)


def get_crawl_urls():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = ('select se_userid,se_sid, se_mid from weibo_search_data where is_crawled = 0 and '
           'se_sourcetype = \'新浪微博\' order by se_createtime desc')
    datas = list()
    with db_execute() as con:
        rs = db_connect.db_queryall(con, sql)
        for r in rs:
            data = {'url': 'http://weibo.com/' + r[0] + '/' + r[1], 'mid': r[2]}
            datas.append(data)
    return datas


def update_weibo_url(mid):
    sql = "update weibo_search_data set is_crawled = 1 where se_mid = :mid"
    args = {'mid': str(mid)}
    with db_execute() as con:
        db_connect.db_dml_parms(con, sql, args)


def get_repost_comment(mid):
    sql = 'select se_repost_count, se_comment_count from weibo_search_data where se_mid = :mid'
    args = dict(mid=mid)
    with db_execute() as con:
        rs = db_connect.db_queryone_params(con, sql, args)
        return rs


def update_repost_comment(**kwargs):
    mid = kwargs.get('mid')
    reposts = kwargs.get('reposts')
    comments = kwargs.get('comments')
    sql = 'select se_repost_count, se_comment_count from weibo_search_data where se_mid = :mid'
    args = dict(mid=mid)
    with db_execute() as con:
        rs = db_connect.db_queryone_params(con, sql, args)
        if reposts != rs[0] or comments != rs[1]:
            update_sql = ('update weibo_search_data set se_repost_count = :reposts, se_comment_count = :comments '
                          'where se_mid = :mid')
            update_args = dict(mid=mid, reposts=reposts, comments=comments)
            db_connect.db_dml_parms(con, update_sql, update_args)


def add_search_cont(search_list):
    save_sql = (
                'insert into weibo_search (mk_primary,mid,murl,create_time,praise_count,repost_count,comment_count,'
                'content,device,user_id,username,uheadimage,user_home,keyword) values(:mk_primary, :mid, '
                ':murl, :create_time, :praise_count,:repost_count, :comment_count, :content, :device, '
                ':user_id, :username,:uheadimage, :user_home, :keyword)'
                )
    with db_execute() as con:

        for search_cont in search_list:
            search_info = {
                'mk_primary': search_cont.mk_primary,
                'mid': search_cont.mid,
                'murl': search_cont.murl,
                'create_time': search_cont.create_time,
                'praise_count': search_cont.praise_count,
                'repost_count': search_cont.repost_count,
                'comment_count': search_cont.comment_count,
                'content': search_cont.content,
                'device': search_cont.device,
                'user_id': search_cont.user_id,
                'username': search_cont.username,
                'uheadimage': search_cont.uheadimage,
                'user_home': search_cont.user_home,
                'keyword': search_cont.keyword
            }
            try:
                db_connect.db_dml_parms(con, save_sql, search_info)
            except Exception as why:
                storage.error('插入出错,具体原因为:{why}, 插入数据是{info}'.format(why=why, info=search_info.__dict__))




