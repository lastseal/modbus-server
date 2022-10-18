# -*- coding: utf-8 -*-

import databank
import logging
import dotenv
import zmq
import os

##
#

dotenv.load_dotenv()

MQ_PORT = int(os.getenv("MQ_PORT"))

##
#

def run():

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://127.0.0.1:{MQ_PORT}")
    
    while True:

        try:

            res = socket.recv_json()

            logging.debug("receive: %s", res)
            
            resType = res['type']

            if resType == 'record':

                cameraId = res['cameraId']
                address = cameraId * 6

                timestamp = res['timestamp']

                ##
                # Separar el timestamp en 2 registros

                b = timestamp.to_bytes(4, 'big')

                ts1 = int.from_bytes(b[0:2], 'big')
                ts2 = int.from_bytes(b[2:], 'big')

                databank.setWord(timestamp, [
                    cameraId,
                    res['DCm'], 
                    res['CCm'], 
                    ts1,
                    ts2
                ])

            elif resType == 'alert':
                databank.activateAlert(res['timestamp'])

        except Exception as ex:
            logging.error(ex)