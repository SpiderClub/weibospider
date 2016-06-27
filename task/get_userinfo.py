# 获取扩散信息
# 后台获取用户信息
import time
import random
from db_operation import weibosearch_dao
from do_dataget import get_userinfo
from db_operation import user_dao
from gl import max_len


def get_users_info(session, headers):
    ids = weibosearch_dao.get_seed_ids()
    users = []
    for uid in ids:
        print(uid)
        time.sleep(random.randint(5, 10))
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