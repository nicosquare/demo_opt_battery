import sqlite3
import logging
from app import app
from .sqlite_init import db_exists
import subprocess

sqlite = app.config["DATABASE_URI"]

def init():
    # check exist database 
    db_exists(sqlite)

init()


def insert_blob(image):
    response = 'OK'
    try:
        # Configure connection object
        sqliteConnection = sqlite3.connect(sqlite)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # save the image in the databases
        sqlite_insert_blob_query = '''UPDATE logotype SET (image) = ? WHERE id = 1'''
        cursor.execute(sqlite_insert_blob_query, (image,))
        # Handle connection close
        sqliteConnection.commit()
        sqliteConnection.close()
        print("Image inserted successfully as a BLOB into a table")
        return response

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        response = str(error)
        return response
           

def read_blob():
    try:
        # Configure connection object
        sqliteConnection = sqlite3.connect(sqlite)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # read the image and send it in binary format
        sqlite_query = '''SELECT image FROM logotype WHERE Id = 1'''
        cursor.execute(sqlite_query)
        img = cursor.fetchall()
        # Handle connection close
        sqliteConnection.commit()
        sqliteConnection.close()
        print("Image successfully")
        response = img[0][0]
        return response    

    except sqlite3.Error as error:
        print("Failed sqlite: ", error)
        response = str(error)
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
        query = '''UPDATE credential SET password  = ? WHERE Id = 1'''
        cur.execute(query, (password,))
        # Handle connection close
        conn.commit()
        conn.close()
    except sqlite3.Error:
        logging.exception("Error running Query")
        return None

def restart_device():
    if app.config["ENV"] == "production":
        try:
            subprocess.run(['/sbin/reboot', '-f'])
            return True
        except subprocess.CalledProcessError:
            logging.exception('Error running subprocess commands')
            return False
    else:
        return True