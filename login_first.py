# coding:utf-8
from tasks import login

if __name__ == '__main__':
    # you should exeute this file, because celery timer wiill execute login delayed
    login.excute_login_task()