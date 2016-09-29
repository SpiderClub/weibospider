# -*-coding:utf-8 -*-
from db_operation import db_connect
from weibo_decorator.decorators import dbtimeout_decorator, save_decorator


@dbtimeout_decorator(2)
def get_crawl_urls():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    # 以下代码是为了测试反爬虫机制注释掉的
    # sql = 'select se_userid,se_sid, se_mid from weibo_search_data where is_crawled = 0 and ' \
    #       'se_sourcetype = \'新浪微博\' order by se_createtime desc'

    sql = 'select se_userid,se_sid, se_mid, se_content from weibo_search_data where is_new = 1 and ' \
          'se_sourcetype = \'新浪微博\' order by se_createtime desc'
    con = db_connect.get_con()
    rs = db_connect.db_queryall(con, sql)
    db_connect.db_close(con)
    datas = []
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
            print('插入出错,具体原因为:{why}'.format(why=why))
            print(search_info.__dict__)
    db_connect.db_close(con)


def get_seed_ids():
    """
    操作weibo_search_data表，获取待爬取用户id队列
    :return:
    """
    truncate_sql = 'truncate table weibo_sinausers_cache'
    insert_sql = 'insert into weibo_sinausers_cache (select se_userid from weibo_search_data where is_new = 1 ' \
                 'and se_sourcetype=\'新浪微博\' group by se_userid)'
    delelte_sql = 'delete from weibo_sinausers_cache where dsu_id in (select su_id from weibo_sina_users)'
    update_sql = 'update weibo_search_data set is_new = 0 where is_new = 1 and se_sourcetype = \'新浪微博\''
    select_sql = 'select dsu_id from weibo_sinausers_cache'
    con = db_connect.get_con()
    db_connect.db_dml(con, truncate_sql)
    print('-----------临时表已清空--------------')
    db_connect.db_dml(con, insert_sql)
    print('-----------临时表数据插入完成--------------')
    db_connect.db_dml(con, delelte_sql)
    print('-----------临时表已去重--------------')
    db_connect.db_dml(con, update_sql)
    print('-----------search表已更新--------------')
    rs = db_connect.db_queryall(con, select_sql)
    print('获取到{num}条需要爬取的id'.format(num=len(rs)))
    db_connect.db_close(con)
    ids = []
    for r in rs:
        ids.append(r[0])
    return ids


if __name__ == '__main__':
    '''
    解决调用 fetchmany()发生LOB variable no longer valid after subsequent fetch 错误的方法
    '''
    sql = 'select se_userid,se_sid, se_mid, se_content from weibo_search_data where is_new = 1 and ' \
          'se_sourcetype = \'新浪微博\' order by se_createtime desc'
    con = db_connect.get_con()
    curs = con.cursor()
    curs.execute(sql)
    for rows in curs:
        print(rows[3])

