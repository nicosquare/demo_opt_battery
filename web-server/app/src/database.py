import sqlite3
import logging
from app import app
from datetime import datetime, timedelta
import socket
import json
from socket import error as socket_error
import subprocess


sqlite = app.config["DATABASE_URI"]


# def convertToBinaryData(filename):
#     #Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData


def insertBLOB(image):
    response = 'OK'
    try:
        sqliteConnection = sqlite3.connect(sqlite)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = '''UPDATE logotype SET (image) = ? WHERE id = 1'''
        cursor.execute(sqlite_insert_blob_query, (image,))
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        response = str(error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
            return response
           

def readBLOB():
    try:
        # Configure connection object
        sqliteConnection = sqlite3.connect(sqlite)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # Update the current form measurements
        sqlite_query = '''SELECT image FROM logotype WHERE Id = 1'''
        cursor.execute(sqlite_query)
        img = cursor.fetchall()
        sqliteConnection.commit()
        # Handle connection close
        print("Image successfully")
        cursor.close()
        response = img[0][0]

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        response = str(error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
            return response    


def read_credential():
    try:
        # Configure connection object
        conn = sqlite3.connect(sqlite)
        cur = conn.cursor()
        # Update the current form measurements
        query = '''SELECT login, password FROM credential WHERE Id = 1'''
        cur.execute(query)
        credential = cur.fetchall()
        # Handle connection close
        conn.commit()
        conn.close()
        return credential
    except sqlite3.Error:
        logging.exception("Error running Query")
        return None


def update_credential(password):
    try:
        # Configure connection object
        conn = sqlite3.connect(sqlite)
        cur = conn.cursor()
        # Update the current form measurements
        query = '''UPDATE credential SET password  = ? WHERE id = 1'''
        cur.execute(query, (password,))
        # Handle connection close
        conn.commit()
        conn.close()
    except sqlite3.Error:
        logging.exception("Error running Query")
        return None


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

