import logging
import os
import shutil

import pytest

from logger import *


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')


@pytest.yield_fixture(scope='module', autouse=True)
def rm_logs():
    yield
    shutil.rmtree(LOG_DIR)


@pytest.mark.parametrize(
    'logger, expected', [
        (crawler_logger, 'crawler'), (parser_logger, 'parser'), (db_logger, 'storage'), (other_logger, 'other')
    ])
def test_loggers(logger, expected):
    assert logger.name == expected
    assert isinstance(logger, logging.Logger)






