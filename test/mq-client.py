# -*- coding: utf-8 -*-
#!/usr/bin/env python

from datetime import datetime

import dotenv
import zmq
import os

dotenv.load_dotenv()

MQ_PORT = int(os.getenv("MQ_PORT"))

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(f"tcp://127.0.0.1:{MQ_PORT}")

'''
socket.send_json({
    "type": "record",
    "cameraId": 0,
    "timestamp": int(datetime.now().timestamp()),
    "DCm": 1,
    "CCm": 2
})
'''

socket.send_json({
    "type": "alert",
    "timestamp": int(datetime.now().timestamp())
})