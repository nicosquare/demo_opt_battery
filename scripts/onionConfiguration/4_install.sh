#!/bin/ash

opkg update
opkg install python3
opkg install python3-pip

pip3 install pysqlite3
pip3 install json5
pip3 install flask
pip3 install waitress



