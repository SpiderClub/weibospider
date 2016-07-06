# -*-coding:utf-8 -*-
from db_operation import db_connect


def get_crawl_urls():
    """
    :return: is_crawled = 0的字段，即需要进行扩散分析的字段
    """
    sql = 'select se_userid,se_sid from weibo_search_data where is_crawled = 0 and ' \
          'se_sourcetype = \'新浪微博\''
    con = db_connect.get_con()
    rs = db_connect.db_queryall(con, sql)
    db_connect.db_close(con)
    urls = []
    for r in rs:
        urls.append('http://weibo.com/' + r[0] + '/' + r[1])
    return urls


def update_weibo_url(mid):
    sql = "update weibo_search_data set is_crawled = 1 where se_mid = :mid"
    args = {'mid': str(mid)}
    con = db_connect.get_con()
    db_connect.db_dml_parms(con, sql, args)
    db_connect.db_close(con)


def get_seed_ids():
    """
    操作weibo_search_data表，获取待爬取用户id队列
    :return:
    """
    truncate_sql = 'truncate table weibo_sinausers_cache'
    insert_sql = 'insert into weibo_sinausers_cache (select se_userid from weibo_search_data where ' \
                 'is_new = 1 and se_sourcetype=\'新浪微博\' group by se_userid)'
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
    rs2 = get_seed_ids()
    print(rs2)