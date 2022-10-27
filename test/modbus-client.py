# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
import sys, os
from datetime import datetime as dt
from datetime import timedelta as td

import socket

registers = [0, 6, 12, 18, 24, 30, 36, 42]

while True:
    ts = dt.now()

    c = ModbusClient('127.0.0.1', 5020, unit_id=2)
    c.open()

    if c.is_open:
        for x in registers:
            regs = c.read_holding_registers(x, 6)    # read function
            if regs:
                print("{:%d/%m/%Y %H:%M:%S} - {}".format(ts, regs))

    time.sleep(1)
        