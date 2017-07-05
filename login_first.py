# coding:utf-8
from tasks import login

if __name__ == '__main__':
    # you should execute this file, because celery timer will execute login delayed
    login.excute_login_task()