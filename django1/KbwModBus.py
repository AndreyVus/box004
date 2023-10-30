#!/usr/bin/python
from pyModbusTCP.client import ModbusClient
import time
import struct
import yaml


def get_param(sma):
	c = ModbusClient(host=sma['ip'], port=sma['port'], timeout=5, auto_open=True, auto_close=True)
	x = ()
	while not x:
		time.sleep(1)
		x = c.read_holding_registers(40072, 37)
	x = struct.unpack('>HHHHhHHHHHHhhhHhhhhhhhIhHhHhhhhhhhhH', struct.pack('>37H', *x))
	return {
	'Devicename': sma["name"],
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
	'Gesamtertrag, MWh': x[22] / 1e4,
	'DC, A': x[24] / 10,
	'DC, V': x[26] / 10,
	'DC, kW': x[28] / 10,
	'Cabinet Temperature, °C': x[30] / 10,
	'Operating State': x[35]
	}


with open("/home/kbwiot/settings.yaml") as file:
	settings = yaml.safe_load(file)
wr_param = [get_param({'name': wr, **settings['SMA'][wr]}) for wr in settings["SMA"].keys()]
ret = {
	**settings["General"],
	**settings["GPS"],
	"Gesamt DC Leistung, kW": sum([float(x["DC, kW"]) for x in wr_param]),
	"Gesamt AC Leistung, kW": sum([float(x["Wirkleistung in Echtzeit, kW"]) for x in wr_param]),
#	"Gesamt Tagesertrag, kWh": sum([float(x["Tagesertrag, kWh"]) for x in wr_param]),
#	"Gesamt Monatsertrag, MWh": sum([float(x["Monatsertrag, kWh"]) for x in wr_param]) / 1000,
#	"Gesamt Jahresertrag, MWh": sum([float(x["Jahresertrag, kWh"]) for x in wr_param]) / 1000,
	"Gesamt Gesamtertrag, MWh": sum([float(x["Gesamtertrag, MWh"]) for x in wr_param]),
	}
for wr in wr_param:
	name = wr.pop('Devicename')
	for k, v in wr.items():
		ret[f"{name} {k}"] = v
print(ret)