import logging
import os
import pymongo
import requests
from time import sleep
from tqdm import tqdm

URL = 'https://developers.onemap.sg/commonapi/search'


def _get_uri():
    username = os.environ.get('MONGODB_USER')
    password = os.environ.get('MONGODB_PASSWORD')
    hostname = os.environ.get('MONGODB_HOST')
    db_name = os.environ.get('MONGODB_NAME')

    logging.info('username=%s', username)
    logging.info('hostname=%s', hostname)
    logging.info('db_name=%s', db_name)

    if not username or not password or not hostname or not db_name:
        logging.error('incomplete mongodb config')

    return f"mongodb+srv://{username}:{password}@{hostname}/{db_name}?retryWrites=true&w=majority"


def _check_postal_code(code):
    payload = {
        'searchVal': code,
        'returnGeom': 'Y',
        'getAddrDetails': 'Y',
        'pageNum': 1
    }
    req = requests.get(URL, params=payload)
    req.raise_for_status()
    return req.json()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                        encoding='utf-8', level=logging.INFO)

    client = pymongo.MongoClient(_get_uri())
    db = client.raw

    start = int(os.environ.get('START', 0))
    end = int(os.environ.get('END', 1000000))
    logging.info('start=%s, end=%s', start, end)

    for i in tqdm(range(start, end)):
        postal_code = '{:06d}'.format(i)
        logging.debug('query=%s', postal_code)

        response = _check_postal_code(postal_code)
        res = db.codes.insert_one(response)
        logging.debug('inserted_id=%s', res.inserted_id)
        sleep(0.1)
