# -*- coding: utf-8 -*-

from pyModbusTCP.server import ModbusServer
from pyModbusTCP.server import DataBank

from datetime import datetime

import databank
import logging
import dotenv
import os

##
#

dotenv.load_dotenv()

MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = int(os.getenv("MODBUS_PORT"))

##
#

class MyDataBank(DataBank):

    def __init__(self):
        super().__init__(virtual_mode=True)

    def get_holding_registers(self, address, number=1, srv_info=None):

        logging.debug("address: %s, number: %s", address, number)

        word = databank.getWord(address)
        logging.debug("word: %s", word)

        return word

##
#

def run():

    server = ModbusServer(MODBUS_HOST, MODBUS_PORT, no_block=True, data_bank=MyDataBank())
    server.start()

    logging.debug("modbus server started")