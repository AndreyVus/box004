#!/usr/bin/python

from pyModbusTCP.client import ModbusClient
import time
import socket
import struct
import syslog
import yaml


def mean(zahlen):
	return sum(zahlen)/len(zahlen)


def get_sma(sma):
	c = ModbusClient(host=sma['ip'], port=sma['port'], timeout=5, auto_open=True, auto_close=True)
	x = ()
	while not x:
		time.sleep(1)
		x = c.read_holding_registers(40072, 37)
	x = struct.unpack('>HHHHhHHHHHHhhhHhhhhhhhIhHhHhhhhhhhhH', struct.pack('>37H', *x))
	return {
		'Devicename'					: sma["name"],
		#'Strom, A'						: x[0] / 10,
		#'Strom PhaseA, A'				: x[1] / 10,
		#'Strom PhaseB, A'				: x[2] / 10,
		#'Strom PhaseC, A'				: x[3] / 10,
		#'Voltage Phase AB, V'			: x[5] / 10,
		#'Voltage Phase BC, V'			: x[6] / 10,
		#'Voltage Phase CA, V'			: x[7] / 10,
		#'Voltage Phase AN, V'			: x[8] / 10,
		#'Voltage Phase BN, V'			: x[9] / 10,
		#'Voltage Phase CN, V'			: x[10] / 10,
		'AC Leistung, kW'				: x[12] / 100,
		#'Frequenz, Hz'					: x[14] / 100,
		#'Blindleistung in Echtzeit, kVAr': x[18] / 100,
		'Gesamtertrag, MWh'				: x[22] / 1e4,
		#'DC, A'						: x[24] / 10,
		#'DC, V'						: x[26] / 10,
		'DC Leistung, kW'				: x[28] / 10,
		'Cabinet Temperature, °C'		: x[30] / 10,
		'Operating State'				: x[35]
	}


def get_refusol(refu):
	def SendRequest(s, param):
		s.sendall(f"{param}\n".encode())
		ret = s.recv(4096).strip(b'\r\n"')
		try:
			return float(ret)
		except ValueError:
			try:
				return ret.decode()
			except UnicodeDecodeError:
				return ret.decode('L1')

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			socket.getaddrinfo(refu["ip"], refu["port"])
		except:
			return {}
		s.connect((refu["ip"], refu["port"]))
		return {
			"Devicename"						: refu["name"],
			#"Zeitstempel"						: SendRequest(s, "REFU.GetTime"),
			#"Einsatzland"						: SendRequest(s, "REFU.COUNTRY.Get"),
			#"MAC-Adresse"						: SendRequest(s, "REFU.I2C5200_EEPROM_GetMacAddress"),
			#"Fimware"							: SendRequest(s, "REFU.GetFirmwareVersion"),
			#"Fimware2"							: SendRequest(s, "REFU.GetStringParameter 0"),
			#"WechselrichterTyp"				: SendRequest(s, "REFU.GetStringParameter 19"),
			#"Device-Revision"					: SendRequest(s, "REFU.GetStringParameter 42"),
			#"Seriennummer"						: SendRequest(s, "REFU.GetStringParameter 43"),
			'Temperatur, °C'			: mean([	SendRequest(s, "REFU.GetParameter 0092, 0") / 10,
													SendRequest(s, "REFU.GetParameter 0092, 1") / 10,
													SendRequest(s, "REFU.GetParameter 0092, 2") / 10,
													SendRequest(s, "REFU.GetParameter 0092, 3") / 10,	]),
			#"T Kühlkörper rechts, °C"			: SendRequest(s, "REFU.GetParameter 0092, 0") / 10,
			#"T oben links, °C"					: SendRequest(s, "REFU.GetParameter 0092, 1") / 10,
			#"T unten rechts, °C"				: SendRequest(s, "REFU.GetParameter 0092, 2") / 10,
			#"T Kühlkörper links, °C"			: SendRequest(s, "REFU.GetParameter 0092, 3") / 10,
			"Status"							: {0: "Initialisierung",
													1: "Ausgeschaltet",
													2: "Aktivierung",
													3: "Betriebsbereit",
													4: "Betrieb",
													5: "Stillsetzen",
													6: "Kurzausfall",
													7: "Störung", }[int(SendRequest(s, "REFU.GetParameter 0501, 0"))],
			#"DC Spannung, V"					: SendRequest(s, "REFU.GetParameter 1104, 0"),
			#"DC Stromstärke, A"				: SendRequest(s, "REFU.GetParameter 1105, 0"),
			"DC Leistung, kW"					: SendRequest(s, "REFU.GetParameter 1106, 0") / 1000,
			"AC Leistung, kW"					: SendRequest(s, "REFU.GetParameter 1107, 0") / 1000,
			#"AC Spannung Peak L1, V"			: SendRequest(s, "REFU.GetParameter 1121, 0"),
			#"AC Spannung Peak L2, V"			: SendRequest(s, "REFU.GetParameter 1121, 1"),
			#"AC Spannung Peak L3, V"			: SendRequest(s, "REFU.GetParameter 1121, 2"),
			#"AC Frequenz L1, Hz"				: SendRequest(s, "REFU.GetParameter 1122, 0"),
			#"AC Frequenz L2, Hz"				: SendRequest(s, "REFU.GetParameter 1122, 1"),
			#"AC Frequenz L3, Hz"				: SendRequest(s, "REFU.GetParameter 1122, 2"),
			#"AC Effektivspannung Mittelwert, V": SendRequest(s, "REFU.GetParameter 1123, 0"),
			#"AC Stromstärke, A"				: SendRequest(s, "REFU.GetParameter 1124, 0"),
			#"AC Stromstärke L1, A"				: SendRequest(s, "REFU.GetParameter 1124, 1"),
			#"AC Stromstärke L2, A"				: SendRequest(s, "REFU.GetParameter 1124, 2"),
			#"AC Stromstärke L3, A"				: SendRequest(s, "REFU.GetParameter 1124, 3"),
			"Tagesertrag, kWh"					: SendRequest(s, "REFU.GetParameter 1150, 0"),
			"Gesamtertrag, MWh"					: SendRequest(s, "REFU.GetParameter 1151, 0") / 1000,
			#"Betriebsstunden, h"				: SendRequest(s, "REFU.GetParameter 1152, 0"),
			"Monatsertrag, MWh"					: SendRequest(s, "REFU.GetParameter 1153, 0") / 1000,
			"Jahresertrag, MWh"					: SendRequest(s, "REFU.GetParameter 1154, 0") / 1000,
			#"Nennleistung, kWp"				: SendRequest(s, "REFU.GetParameter 1155, 0"),
			#"Leistungsbegrenzung, %"			: SendRequest(s, "REFU.GetParameter 1162, 0") / 10,
			#"EinstrahlSensor, W/m²"			: SendRequest(s, "REFU.GetParameter 1191, 0"),
			#"Temperatur, °C"					: SendRequest(s, "REFU.GetParameter 1193, 0"),
		}


def get_param(wr):
	if wr['Type'] == 'SMA':
		return get_sma(wr)
	elif wr['Type'] == 'Refusol':
		return get_refusol(wr)


try:
	with open("/home/kbwiot/settings.yaml") as file:
		settings = yaml.safe_load(file)
	wr_param = [get_param({'name': wr, **settings['Solar'][wr]}) for wr in settings["Solar"].keys()]
	ret = {
		**settings["General"],
		**settings["GPS"],
		"Gesamt DC Leistung, kW": sum([float(x["DC Leistung, kW"]) for x in wr_param]),
		"Gesamt AC Leistung, kW": sum([float(x["AC Leistung, kW"]) for x in wr_param]),
		"Gesamt Gesamtertrag, MWh": sum([float(x["Gesamtertrag, MWh"]) for x in wr_param]),
	}
	if all(["Jahresertrag, MWh" in k for k in wr_param]):
		ret.update({
			"Gesamt Tagesertrag, kWh": sum([float(x["Tagesertrag, kWh"]) for x in wr_param]),
			"Gesamt Monatsertrag, MWh": sum([float(x["Monatsertrag, MWh"]) for x in wr_param]),
			"Gesamt Jahresertrag, MWh": sum([float(x["Jahresertrag, MWh"]) for x in wr_param]),
		})
	for wr in wr_param:
		name = wr.pop('Devicename')
		for k, v in wr.items():
			ret[f"{name} {k}"] = v
	print(ret)
except Exception as e:
	syslog.syslog(syslog.LOG_WARNING, f"Solar.py: {e}")