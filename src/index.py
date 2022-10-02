# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pyModbusTCP.server import ModbusServer
from pyModbusTCP.server import DataBank
from server import Server
from datetime import datetime
from datetime import timedelta

import argparse
import logging
import dotenv
import signal
import sched
import time
import sys
import os

##
#

dotenv.load_dotenv()

MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = int(os.getenv("MODBUS_PORT"))

TIMESTAMP_GTE = int(os.getenv("TIMESTAMP_GTE"))
ALERT_GTE = int(os.getenv("ALERT_GTE"))

LOG_LEVEL = (os.getenv("LOG_LEVEL") or 'INFO').lower()

logging.basicConfig(
    format='%(asctime)s.%(msecs).03d %(levelname)s - %(message)s', 
    level=logging.DEBUG if LOG_LEVEL == 'debug' else logging.INFO
)

records = [ {"cameraId": i, "DCm": 0, "CCm": 0, "timestamp": now} for i in range(8)]
alert = { "value": 0, "message": None, "timestamp": now}

##
#

def setWord(doc):

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

def cleanDoc(cameradId):

    logging.debug("cleaning record of %d", cameraId)

    word = [cameraId, 0, 0, 0, 0, 0 if alert is None else 1]

    DataBank.set_words(cameraId * 6, [
        cameraId, 
        0, 
        0, 
        0, 
        0, 
        0 if alert is None else 1
    ])

##
#

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', action='store_true')

    args = parser.parse_args()

    try:

        server = ModbusServer(MODBUS_HOST, MODBUS_PORT, no_block=True)
        server.start()

        server_pull = Server()

        now = datetime.now()

        sched1 = sched.scheduler(time.time, time.sleep)
        sched1.run()

        while True:

            try:

                doc = server_pull.listening()
                logging.info("doc: %s", doc)

                docType = doc['type']

                if docType == "alert":
                    alert['value'] = 1
                    alert['message'] = doc['message']
                    alert['timestamp'] = datetime.now()

                    sched1.enter(ALERT_GTE*60, 1, cleanAlertFlag)

                elif docType == "record":
                    #timestamp = int(doc['timestamp'].timestamp())

                    setWord(doc)

                    sched1.enter(TIMESTAMP_GTE*60, 1, cleanDoc, kwargs={
                        'cameraId': doc['cameraId']
                    })

                else:
                    logging.warning("data not support")
 
            except Exception as ex:
                logging.error(ex)

    except Exception as ex:

        logging.error(ex)
        server.stop()

##
#

def handle_sigint(signum, frame):
    logging.info("sigint received (%d)", signum)
    sys.exit(0)

def handle_sigterm(signum, frame):
    logging.warning("sigterm received (%d)", signum)
    sys.exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT,  handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    main()
