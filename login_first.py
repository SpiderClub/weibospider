# coding:utf-8
from tasks import login

if __name__ == '__main__':
    # 由于celery的定时器有延迟，所以第一次需要手动
    login.excute_login_task()