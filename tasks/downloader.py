# this task is used to download large files, such as images
import os
import shutil

import requests

from logger import crawler_logger
from config import (
    image_type, images_path
)
from .workers import app


@app.task(ignore_result=True)
def download_img_task(mid, urls):
    count = 0
    for img_url in urls:
        if image_type == 'large':
            img_url = img_url.replace('thumbnail', 'large').replace('square', 'large')
        suffix = img_url[img_url.rfind('.') + 1:]
        # skip gif images, which is used to show loading process
        if suffix != 'gif':
            count += 1
            try:
                image_response = requests.get(img_url, stream=True)
            except Exception as e:
                crawler_logger.error('fail to down image {}, {} is raised'.format(img_url, e))
            else:
                with open(os.path.join(images_path, '{}-{}.{}'.
                          format(mid, count, suffix)), 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
