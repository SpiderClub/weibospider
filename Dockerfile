FROM ubuntu:16.04

MAINTAINER ResolveWang <w1796246076@sina.com>

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    ' > /etc/apt/sources.list

RUN apt update
RUN apt install python3 python3-pip -yq
RUN which python3|xargs -i ln -s {} /usr/bin/python
RUN which pip3|xargs -i ln -s {} /usr/bin/pip
COPY ./WeiboSpider/ /home/WeiboSpider
WORKDIR /home/WeiboSpider
RUN pip install -r requirements.txt
CMD ["celery", "-A", "tasks.workers", "worker", "-l", "info", "-c", "1"]
