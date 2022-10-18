# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pymongo import MongoClient
from datetime import datetime
import pymongo

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

dsn = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

print("Connecting")

client = MongoClient(dsn)

db = client["camaras"]
collection = db["registros"]

collection.create_index("cameraId")
collection.create_index("timestamp")    

print("results", datetime.now())
