#!/bin/ash

opkg update
opkg install python3
opkg install python3-pip

pip3 install pyserial
pip3 install logging
pip3 install future
pip3 install pysqlite3
pip3 install times
pip3 install smbus2
pip3 install pathlib
pip3 install json5
pip3 install ibmiotf
pip3 install paho_mqtt
pip3 install schedule
pip3 install flask
pip3 install waitress



