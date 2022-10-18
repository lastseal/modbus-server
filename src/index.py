# -*- coding: utf-8 -*-
#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta

import modbus
import mq

import argparse
import logging
import dotenv
import signal
import time
import sys
import os

##
#

dotenv.load_dotenv()

LOG_LEVEL = (os.getenv("LOG_LEVEL") or 'INFO').lower()

logging.basicConfig(
    format='%(asctime)s.%(msecs).03d %(levelname)s - %(message)s', 
    level=logging.DEBUG if LOG_LEVEL == 'debug' else logging.INFO
)

##
#
'''
def setWord(doc, alert):

    cameraId = doc['cameraId']

    b = doc['timestamp'].to_bytes(4, 'big')

    ts1 = int.from_bytes(b[0:2], 'big')
    ts2 = int.from_bytes(b[2:], 'big')

    word = [
        cameraId,
        doc['DCm'], 
        doc['CCm'], 
        ts1,
        ts2,
        alert['value']
    ]                    

    index = cameraId * 6

    DataBank.set_words(index, word)

##
#

def cleanAlertFlag():

    logging.debug("cleaning alert flag")

    for cameraId in range(8):
        DataBank.set_words(cameraId * 6, [
            cameraId, 
            0,          # DCm
            0,          # CCm
            0,          # TS1
            0,          # TS2
            0           # Alert flag
        ])

##
#

def cleanDoc(cameraId, alert):

    logging.debug("cleaning record of %d", cameraId)

    word = [cameraId, 0, 0, 0, 0, 0 if alert is None else 1]

    DataBank.set_words(cameraId * 6, [
        cameraId, 
        0, 
        0, 
        0, 
        0, 
        alert
    ])
'''

##
#

def handle_sigint(signum, frame):
    logging.info("sigint received (%d)", signum)
    sys.exit(0)

def handle_sigterm(signum, frame):
    logging.info("sigterm received (%d)", signum)
    sys.exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT,  handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:

        modbus.run()
        mq.run()

    except Exception as ex:
        logging.error(ex)
