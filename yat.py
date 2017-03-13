# 这是耦合的另外一个程序的代码,sqlite同样依赖于另一个程序的位置
import sqlite3


class SqliteDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('/home/wpm/project/weiboupdate/weibo')

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def _close(self):
        self.conn.close()


class WeiboUrl(object):
    __slots__ = ('_url', '_mid')

    def __init__(self, url, mid):
        self._url = url
        self._mid = mid

    def store(self):
        """
        :return: 存储新任务
        """
        sql = 'insert into task (url, mid) values (?, ?)'
        with SqliteDB() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (self._url, self._mid))
            conn.commit()



