# this task is used to download large files, such as images
import os
import shutil

import requests
from celery import group

from ..logger import crawler_logger
from ..db.dao import WbDataOper
from ..config import (
    image_type, images_path
)
from .workers import app


@app.task
def download_img(mid, urls):
    count = 0
    urls = urls.split(';')
    for img_url in urls:
        if image_type == 'large':
            img_url = img_url.replace('thumbnail', 'large').\
                replace('square', 'large')
        suffix = img_url[img_url.rfind('.') + 1:]
        # skip gif images, which is used to show loading process
        if suffix != 'gif':
            count += 1
            try:
                image_response = requests.get(img_url, stream=True)
            except Exception as e:
                crawler_logger.error('fail to down image {}, {} '
                                     'is raised'.format(img_url, e))
            else:
                with open(os.path.join(images_path, '{}-{}.{}'.
                          format(mid, count, suffix)), 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
    WbDataOper.set_img_downloaded(mid)


@app.task
def execute_download_task():
    datas = WbDataOper.get_img_not_download()
    caller = group(download_img.s(data.weibo_id, data.weibo_img) for
                   data in datas)
    caller.delay()