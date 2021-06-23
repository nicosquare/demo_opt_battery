import logging
from app import app
from datetime import datetime, timedelta
from socket import error as socket_error
import subprocess

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
        data = {
            'NetWorks': [{'key': 1, 'name': '4C1C90'},
                         {'key': 2, 'name': 'MARIA'},
                         {'key': 3, 'name': 'YOLANDA SUAREZ'},
                         {'key': 4, 'name': 'Luz_Elvira'},
                         {'key': 5, 'name': 'PPGOLDEN-2G'},
                         {'key': 6, 'name': 'MAO CASA 2.4'},
                         {'key': 7, 'name': 'Maye Perez'},
                         {'key': 8, 'name': 'OSITOS'},
                         {'key': 9, 'name': 'Omega-49FD'},
                         {'key': 10, 'name': 'IGLESIAS_SERRANO'},
                         {'key': 11, 'name': 'FAMILIA_ROBAYO'},
                         {'key': 12, 'name': 'FAMILIABORBON'},
                         {'key': 13, 'name': 'AZUMI'},
                         {'key': 14, 'name': 'Zapata Isaza 2.4G_ETB'}]}

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
