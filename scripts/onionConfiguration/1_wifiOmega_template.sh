#!/bin/ash

echo Configuration wifi
wifisetup add -ssid something -encr psk2 -password dante
wifisetup priority -ssid something -move top
