import logging
import math
import os
import pymongo
import requests
import time
from datetime import datetime
from multiprocessing import Pool

URL = 'https://developers.onemap.sg/commonapi/search'
MIN = 0
MAX = 1000000


def _get_uri():
    username = os.environ.get('MONGODB_USER')
    password = os.environ.get('MONGODB_PASSWORD')
    hostname = os.environ.get('MONGODB_HOST')
    db_name = os.environ.get('MONGODB_NAME')

    if not username or not password or not hostname or not db_name:
        logging.error('incomplete mongodb config')

    return f"mongodb+srv://{username}:{password}@{hostname}/{db_name}?retryWrites=true&w=majority"


def _round_to_hundreds(x):
    return math.ceil(x / 100) * 100


def _get_range():
    size = MAX - MIN
    runs = 28 * 24 * 2 * 2 # over 2x28 days and 24 hours each over 2 months
    size_per_run = _round_to_hundreds(size / runs)

    now = datetime.utcnow()
    i = ((now.day % 28) + 1) * now.hour
    i2 = ((now.day % 28) + 1) * (now.hour + 1)
    return i * size_per_run, i2 * size_per_run


def _get_pool_size(rate):
    return math.ceil(rate / 5)


def _check_postal_code(code):
    assert isinstance(code, int)

    payload = {
        'searchVal': '{:06d}'.format(code),
        'returnGeom': 'N',
        'getAddrDetails': 'Y',
        'pageNum': 1
    }
    req = requests.get(URL, params=payload)
    req.raise_for_status()

    time.sleep(0.1)
    print('.', flush=True, end='', sep='')

    return payload | req.json()


def _get_bulk_delete(codes):
    return [pymongo.DeleteMany({'searchVal': c}) for c in codes]


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                        encoding='utf-8', level=logging.INFO)

    client = pymongo.MongoClient(_get_uri())
    db = client.raw
    db.codes.delete_many({'found': 0})

    start, end = _get_range()
    start = int(os.environ.get('START', start))
    end = int(os.environ.get('END', end))
    logging.info('start=%s, end=%s', start, end)

    pool_size = _get_pool_size((end - start) / 60)
    logging.info('pool_size=%s', pool_size)

    with Pool(pool_size) as p:
        responses = p.map(_check_postal_code, range(start, end))
        db.codes.bulk_write(_get_bulk_delete(range(start, end)))
        db.codes.insert_many(responses)

    logging.info('count=%s', db.codes.count_documents({}))
