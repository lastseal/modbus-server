#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import pymongo
import json

host = "127.0.0.1"
port = 27017

dbname = "camaras"
collectionName = "registros"

try:
    client = pymongo.MongoClient(f"mongodb://{host}:{port}")

    db = client[dbname]
    collection = db[collectionName]

    gte = datetime.strptime("2022-04-05 00:00:00", "%Y-%m-%d %H:%M:%S")
    lte = datetime.strptime("2022-04-05 23:59:59", "%Y-%m-%d %H:%M:%S")

    docs = collection.find({
            'timestamp': {
                '$gte': gte,
                '$lte': lte
            }
        }, 
        sort=[( 'timestamp', pymongo.DESCENDING )]
    )

    data = [ dict(x) for x in docs ]

    print( json.dumps(data, default=str) )

except Exception as ex:
    print(ex)