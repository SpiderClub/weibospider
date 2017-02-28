# -*-coding:utf-8 -*-
from db_operation import db_connect
from logger.log import parser
from weibo_decorator.decorators import dbtimeout_decorator, save_decorator


@dbtimeout_decorator(2)
def get_crawl_urls():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = ('select se_userid,se_sid, se_mid from weibo_search_data where is_crawled = 0 and '
           'se_sourcetype = \'新浪微博\' order by se_createtime desc')

    con = db_connect.get_con()
    rs = db_connect.db_queryall(con, sql)
    db_connect.db_close(con)
    datas = list()
    for r in rs:
        data = {'url': 'http://weibo.com/' + r[0] + '/' + r[1], 'mid': r[2]}
        datas.append(data)
    return datas


@dbtimeout_decorator(0)
def update_weibo_url(mid):
    sql = "update weibo_search_data set is_crawled = 1 where se_mid = :mid"
    args = {'mid': str(mid)}
    con = db_connect.get_con()
    db_connect.db_dml_parms(con, sql, args)
    db_connect.db_close(con)


@dbtimeout_decorator(0)
def update_weibo_repost(mid, reposts_count):
    sql = 'select se_repost_count from weibo_search_data where se_mid = :mid'
    args = {'mid': str(mid)}
    con = db_connect.get_con()
    rs = db_connect.db_queryone_params(con, sql, args)
    if reposts_count != rs[0]:
        update_sql = 'update weibo_search_data set se_repost_count = :reposts_count where se_mid = :mid'
        update_args = {'mid': mid, 'reposts_count': reposts_count}
        db_connect.db_dml_parms(con, update_sql, update_args)
    db_connect.db_close(con)


@save_decorator
def add_search_cont(search_list):
    save_sql = 'insert into weibo_search (mk_primary,mid,murl,create_time,praise_count,repost_count,comment_count,' \
               'content,device,user_id,username,uheadimage,user_home,keyword) values(:mk_primary, :mid, ' \
               ':murl, :create_time, :praise_count,:repost_count, :comment_count, :content, :device, ' \
               ':user_id, :username,:uheadimage, :user_home, :keyword)'

    con = db_connect.get_con()

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
            parser.error('插入出错,具体原因为:{why}, 插入数据是{info}'.format(why=why, info=search_info.__dict__))
    db_connect.db_close(con)




