# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

import logging
import dotenv
import os

##
#

dotenv.load_dotenv()

TIMESTAMP_GTE = timedelta(minutes=int(os.getenv("TIMESTAMP_GTE")))
ALERT_GTE = timedelta(minutes=int(os.getenv("ALERT_GTE")))

##
#

data = []

now = datetime.now()

for cameraId in range(8):
    data.append({
        'address': cameraId * 6,
        'updated_at': now - TIMESTAMP_GTE,
        'alerted_at': now - ALERT_GTE,
        'word': [cameraId, 0, 0, 0, 0, 0]
    })

##
#

def getWord(address):
    
    addresses = [ x['address'] for x in data ]

    if address not in addresses:
        raise Exception(f"address: {address} doesn't exist")

    index = addresses.index(address)

    item = data[index]
    word = item['word']
    now = datetime.now()

    gte = now - ALERT_GTE

    word[5] = 1 if item['alerted_at'] > gte else 0

    gte = now - TIMESTAMP_GTE

    return word if item['updated_at'] > gte else [word[0], 0, 0, 0, 0, word[5]]

##
#    

def setWord(timestamp, word):

    cameraId = word[0]

    logging.debug("cameraId: %s - %s", cameraId, word)

    if cameraId < 0 or cameraId >= len(data):
        raise Exception(f"cameraId: {cameraId} doesn't exist")
    
    tmp = data[cameraId]['word']

    for i in range(len(word)):
        tmp[i] = word[i]

    data[cameraId]['word'] = tmp
    data[cameraId]['updated_at'] = datetime.fromtimestamp(timestamp)

##
#

def activateAlert(timestamp):
    for item in data:
        item['alerted_at'] = datetime.fromtimestamp(timestamp)
