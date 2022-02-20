# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta

import pymongo
import dotenv
import os

dotenv.load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = "127.0.0.1"
MONGO_PORT = int(os.getenv("MONGO_PORT"))

dsn = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(dsn)

db = client["camaras"]
collection = db["alertas"]

gte = datetime.now() - timedelta(days=10)

print( collection.find_one(
    {'timestamp': {'$gte': gte}}, 
    sort=[( 'timestamp', pymongo.DESCENDING )]
) )