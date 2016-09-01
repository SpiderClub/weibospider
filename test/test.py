from multiprocessing import Process, Queue
from time import sleep


def produce(q):
    q.put('test')
    print('produce ...')
    sleep(10)
    print('produce已经睡眠了10s')


def consumer(q):
    v = q.get(True)
    print(v)
    sleep(8)
    print('consumer已经睡眠了8s')


def time_task():
    sleep(3)
    print('time_task已经睡眠了3s')


class A(object):
    def __init__(self):
        self.t1 = ''
        self.t2 = 0
        self.t3 = ''

    def test(self):
        print('hello')

if __name__ == '__main__':
    a = A()
    a.t3 = None
    print(a.__dict__['t1'] == '')
    for x in dir(a):
        print(getattr(A, x))