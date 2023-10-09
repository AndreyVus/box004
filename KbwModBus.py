#!/usr/bin/python
# http://10.8.0.50:8003/#/
from pyModbusTCP.client import ModbusClient
#from pyModbusTCP.utils import word_list_to_long
import time
import sys
import syslog
import numpy as np
import struct
import numpy

c = ModbusClient(host="192.168.10.20", port=502, timeout=5, auto_open=True, auto_close=True)  # , debug=True)
f = open("KbwModBus.txt", "wb")
for a in range(40000,41400,125):
	print(a)
	for to in range(1, 6):
		time.sleep(to)
		print('.')
		b = c.read_holding_registers(a, 125)
		if b:
			break
	if b:
		f.write(struct.pack('<125H',*b))
			#f"{numpy.array([hex(b1) for b1 in b])}\n")
		print('ok')
	else:
		print(f"{s} {c.last_error_as_txt}")
f.close()
print('end')

def rh(name, addr, lange):
	s = f"rh('{name}', {addr}, {lange})"
	for to in range(1, 6):
		time.sleep(to)
		x = c.read_holding_registers(addr, lange)
		if x:
			break
	if x:
		#	f.write(s+'\n')
		if lange == 2:
			y = word_list_to_long(x, big_endian=True)
		elif lange == 4:
			y = word_list_to_long(x, big_endian=True, long_long=True)
		else:
			y = list(map(hex,x))
		print(f"{s} {y}")
		#syslog.syslog(syslog.LOG_INFO, f"KbwModBus {s} {y}")
	else:
		print(f"{s} {c.last_error_as_txt}")#syslog.syslog(syslog.LOG_INFO, f"KbwModBus {c.last_error_as_txt}")


t="""Amps (A)
Amps PhaseA (AphA)
Amps PhaseB (AphB)
Amps PhaseC (AphC)
A_SF
Phase Voltage AB (PPVphAB)
Phase Voltage BC (PPVphBC)
Phase Voltage CA (PPVphCA)
Phase Voltage AN (PhVphA)
Phase Voltage BN (PhVphB)
Phase Voltage CN (PhVphC)
V_SF
Watts (W)
W_SF
Hz
Hz_SF
VA
VA_SF
VAr
VAr_SF
PF
PF_SF
WattHours (WH)
WH_SF
DC Amps (DCA)
DCA_SF
DC Voltage (DCV)
DCV_SF
DC Watts (DCW)
DCW_SF
Cabinet Temperature (TmpCab)
Heat Sink Temperature (TmpSnk)
Transformer Temperature (TmpTrns)
Other Temperature (TmpOt)
Tmp_SF
Operating State (St)"""
#m=[0,0,0.1,0.1,0.1,0.1,0,0.1,0.1,0.1,0.1,0.1,0.1,0,10,0,0.01,0,10,0,10,0,0.001,0,0.1,0,0.1,0,0.1,0,0.1,0,0.1,0,0,0,0,1]
#x=struct.unpack('>HHHHhHHHHHHhhhHhhhhhhhIhHhHhhhhhhhhH', struct.pack('>37H', *c.read_holding_registers(40072, 37)))
#for t1,m1,x1 in zip(t.split('\n'), m, x):
#	if m1>0:
#		print(t1, m1*x1)
#time.sleep(1)
#print(f"Gesamtertrag {struct.unpack('>Q', struct.pack('>4H', *c.read_holding_registers(40187, 4)))[0]/1e3:1.1f} kWh")
#time.sleep(1)

#print([x/10 for x in c.read_holding_registers(40072, 37)])
