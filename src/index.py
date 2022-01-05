# -*- coding: utf-8 -*-

#!/usr/bin/env python

from pyModbusTCP.server import ModbusServer, DataBank
from pymongo import MongoClient

import argparse
import logging
import pymongo
import dotenv
import signal
import time
import sys
import os

##
#

dotenv.load_dotenv()

MODBUS_HOST = os.getenv("MODBUS_HOST")
MODBUS_PORT = int(os.getenv("MODBUS_PORT"))

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_POLL = int(os.getenv("MONGO_POLL"))

LOG_LEVEL = (os.getenv("LOG_LEVEL") or 'INFO').lower()

logging.basicConfig(
    format='%(asctime)s.%(msecs).03d %(levelname)s - %(message)s', 
    level=logging.DEBUG if LOG_LEVEL == 'debug' else logging.INFO
)

##
#

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--auth', action='store_true')

    args = parser.parse_args()
    print(args)

    try:

        if args.auth:
            dsn = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"
        else:
            dsn = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

        client = MongoClient(dsn)

        logging.info("Mongo DB connected to %s", dsn)

        db = client["pollos"]
        collection = db["registros"]

        duration = 0.2
        counter = 0

        '''
        collection.insert_one({
            "cameraId": 1, 
            "xCm": 10, 
            "yCm": 10, 
            "timestamp": 1641418302778
        })
        '''

        server = ModbusServer(MODBUS_HOST, MODBUS_PORT, no_block=True)
        server.start()

        logging.info("Modbus server listen in %s:%s", MODBUS_HOST, MODBUS_PORT)

        while True:

            try:
                if counter > MONGO_POLL:
                    doc = collection.find_one(sort=[( '_id', pymongo.DESCENDING )])
                    logging.debug("%s", doc)

                    counter = 0

                    cameraId = doc['cameraId']
                    

                    DataBank.set_words(4, [
                        cameraId, 
                        doc['xCm'], 
                        doc['yCm'], 
                        doc['timestamp']
                    ])

                time.sleep(duration)

                counter += duration

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
