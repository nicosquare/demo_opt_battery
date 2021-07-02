#!/bin/ash

echo Configuration wifi
if [ $1 ];
then
  if [ $2 ];
  then
  wifisetup add -ssid $1 -encr psk2 -password $2
  wifisetup priority -ssid $1 -move top
  else
  echo Not network password
  fi
else
echo Not network name 
fi
