import paho.mqtt.publish as publish
import psutil
import requests
import subprocess

def get_ssid():
    try:
        return subprocess.check_output(["iwgetid", "-r"]).decode().strip()
    except:
        return "no"

if 200 == requests.get("http://10.8.0.1:8055", timeout=5).status_code:
    publish.single("LED_VPN", 1, hostname="localhost")
    vpn_addr = psutil.net_if_addrs().get("tun0", [""])[0].address
else:
    publish.single("LED_VPN", 0, hostname="localhost")
    vpn_addr = ""
with open("/proc/stat", "r") as f:
    for line in f:
        if line.startswith("cpu "):
            values = line.split()
            print({"IP VPN": vpn_addr,
"WLAN LTE Status": get_ssid(),
"Free RAM, b": psutil.virtual_memory().free,
"Free Disk, b": psutil.disk_usage(".").free,
"CPU Temperatur, °C": subprocess.check_output(["vcgencmd", "measure_temp"]).decode()[5:-3],
"CPU Usage, %": round((int(values[1]) + int(values[3])) * 100 / (int(values[1]) + int(values[3]) + int(values[4])), 1)})
            break