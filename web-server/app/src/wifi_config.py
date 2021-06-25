import logging
from app import app
from datetime import datetime, timedelta
from socket import error as socket_error
import subprocess
import os
import os.path as path
import json

dir_name = os.path.dirname(path.abspath(__file__))
wifi_data_development = '/utils/'.join([dir_name, 'data.json'])

def scan_wifi_networks():
    if app.config["ENV"] == "production":
        try:
            result = subprocess.run(
                ["wifisetup"], input=b"1", stdout=subprocess.PIPE
            )

            response = result.stdout
            responseDecode = response.decode("utf-8")
            ini_networks = responseDecode.find('Select Wifi network:')
            len_ini = len('Select Wifi network:')
            end_networks = responseDecode.find('Selection: >')
            Networks = responseDecode[(ini_networks + len_ini):end_networks]
            NameNetworks = Networks.split('\n')

            wifiNetworks = []
            key = 1
            for net in NameNetworks:
                if net != '':
                    NetW = net.split(') ')
                    network = {'key': key, 'name': NetW[1]}
                    wifiNetworks.append(network)
                    key = key + 1

            data = {'NetWorks': wifiNetworks}
        except subprocess.CalledProcessError:
            logging.exception('Error running subprocess commands')
            return {'NetWorks': []}
    else:
        # read file "data.json" for send wifi networks example
        f = open(wifi_data_development, "r")
        content = f.read()
        data = json.loads(content)
    return data


def config_wifi(wifi_name, password):
    if app.config["ENV"] == "production":
        try:
            subprocess.run(
                ['/usr/bin/wifisetup', 'add', '-ssid', wifi_name, '-encr', 'psk2', '-password', password])
            subprocess.run(['/usr/bin/wifisetup', 'priority', '-ssid', wifi_name, '-move', 'top'])
            # subprocess.run(['/sbin/reboot', '-f'])
            return True
        except subprocess.CalledProcessError:
            logging.exception('Error running subprocess commands')
            return False
    else:
        return True
