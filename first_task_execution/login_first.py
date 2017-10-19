import sys

sys.path.append('.')
sys.path.append('..')

from tasks import execute_login_task

if __name__ == '__main__':
    # you should execute this file, because celery timer will execute login delayed
    execute_login_task()
