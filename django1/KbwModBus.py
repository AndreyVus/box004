#!/usr/bin/python

from pyModbusTCP.client import ModbusClient
import time
import struct

c = ModbusClient(host="192.168.10.20", port=502, timeout=5, auto_open=True, auto_close=True)
x = ()
while not x:
	time.sleep(1)
	x = c.read_holding_registers(40072, 37)
x = struct.unpack('>HHHHhHHHHHHhhhHhhhhhhhIhHhHhhhhhhhhH', struct.pack('>37H', *x))

print({
	'Strom, A': x[0] / 10,
	'Strom PhaseA, A': x[1] / 10,
	'Strom PhaseB, A': x[2] / 10,
	'Strom PhaseC, A': x[3] / 10,
	'Voltage Phase AB, V': x[5] / 10,
	'Voltage Phase BC, V': x[6] / 10,
	'Voltage Phase CA, V': x[7] / 10,
	'Voltage Phase AN, V': x[8] / 10,
	'Voltage Phase BN, V': x[9] / 10,
	'Voltage Phase CN, V': x[10] / 10,
	'Wirkleistung in Echtzeit, kW': x[12] / 100,
	'Frequenz, Hz': x[14] / 100,
	'Blindleistung in Echtzeit, kVAr': x[18] / 100,
	'Gesamtertrag, MWH': x[22] / 1e4,
	'DC, A': x[24] / 10,
	'DC, V': x[26] / 10,
	'DC, kW': x[28] / 10,
	'Cabinet Temperature, °C': x[30] / 10,
	'Operating State': x[35]
})