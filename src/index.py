# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pyModbusTCP.server import ModbusServer
from pyModbusTCP.server import DataBank
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta


import argparse
import logging
import pymongo
import dotenv
import signal
import time
import sys
import os

from server import Server

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

##
#

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', action='store_true')

    args = parser.parse_args()

    try:

        duration = 0.2
        counter = 10
        MONGO_POLL = 100

        server = ModbusServer(MODBUS_HOST, MODBUS_PORT, no_block=True)
        server.start()

        server_pull = Server()
       
        while True:

            try:
            
                counter = 0
                now = datetime.now()
                response = server_pull.listening()
                print(response)

                gte = now - timedelta(minutes=ALERT_GTE)
                
                alert = alerts.find_one(
                    {'timestamp': {'$gte': gte}}, 
                    sort=[( 'timestamp', pymongo.DESCENDING )]
                )

                gte = now - timedelta(minutes=TIMESTAMP_GTE)

                for cameraId in range(8):
                
                    doc = records.find_one(
                        {'cameraId':cameraId, 'timestamp': {'$gte': gte}}, 
                        sort=[( 'timestamp', pymongo.DESCENDING )]
                    )

                    if doc is not None:

                        logging.debug("%s", doc)

                        timestamp = int(doc['timestamp'].timestamp())

                        ##
                        # Separar el timestamp en 2 registros

                        b = timestamp.to_bytes(4, 'big')

                        ts1 = int.from_bytes(b[0:2], 'big')
                        ts2 = int.from_bytes(b[2:], 'big')

                        word = [
                            doc['cameraId'],
                            doc['DCm'], 
                            doc['CCm'], 
                            ts1,
                            ts2,
                            0 if alert is None else 1
                        ]

                    else:

                        logging.debug("Data not found for cameraId %d", cameraId)

                        word = [cameraId, 0, 0, 0, 0, 0 if alert is None else 1]

                    index = cameraId * 6

                    DataBank.set_words(index, word)

 
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
