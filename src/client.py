# -*- coding: utf-8 -*-

# read_register
# read registers and print result on stdout

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
import sys, os
from datetime import datetime as dt
from datetime import timedelta as td

import socket

devices = {
    0: {'host': '127.0.0.1', 'port': 5020, 'id': 2, 'name': 'dev0'},
}
registers = [0, 5, 10, 15, 20, 25, 30]

ts = dt.now()

for dev in devices:

    c = ModbusClient()

    # uncomment this line to see debug message
    #c.debug(True)

    # define modbus server host, port, ID
    c.host(devices[dev]['host'])
    c.port(devices[dev]['port'])
    c.unit_id(devices[dev]['id'])

    energy = []

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to {}:{}".format(devices[dev]['host'], devices[dev]['port']))

    # if open() is ok, read register
    if c.is_open():
        for x in registers:
            # read 4 registers at address x, store result in regs list
            regs = c.read_holding_registers(x, 5)    # read function
            if regs:
                print("{:%d/%m/%Y %H:%M:%S} - {}".format(ts, regs))
    