# coding:utf-8
# 获取扩散信息
# 后台获取用户信息
import logging, time
from db_operation import weibosearch_dao
from do_dataget import get_userinfo
from db_operation import user_dao
from gl import max_len, headers, count


def get_users_info(q):
    session = q.get()
    logging.info('本次抓取时间为:{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    ids = weibosearch_dao.get_seed_ids()
    users = []
    for uid in ids:
        print(uid)
        user = get_userinfo.get_profile(user_id=uid, session=session, headers=headers)
        if user is not None:
            users.append(user)
        if len(users) == max_len:
            user_dao.save_users(users)
            users = []
            print('已经插入{num}条数据'.format(num=max_len))

    # 保存剩下的
    if len(users) > 0:
        user_dao.save_users(users)
    print('本次抓取结束,结束时间为{curtime}'.format(curtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    logging.info('本次抓取结束，时间是:{curtime}，一共抓取了{count}个页面'.format(curtime=time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime()), count=count))