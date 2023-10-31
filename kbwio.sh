#!/bin/bash
echo "[Unit]
Description=kbwio
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/kbwiot
ExecStart=/home/kbwiot/KbwIO.py

[Install]
WantedBy=default.target
">/etc/systemd/system/
systemctl enable kbwio.service
systemctl start kbwio.service
systemctl status kbwio.service