'''
test logger
'''
from log import crawler, parser, storage, other

crawler.info('this is crawler')

parser.info('this is parser')

storage.info('this is storage')

other.info('this is other')
