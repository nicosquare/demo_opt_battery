import sqlite3
import logging
from urllib.request import pathname2url
import os
import os.path as path


sqlite = '/mnt/g/escritorio/database-egeo/EGEO.sqlite'

dir_name = os.path.dirname(path.abspath(__file__))
db_script_hard_reset = '/../../../scripts/database/'.join([dir_name, 'first_configuration.sql'])
img = '/../../../scripts/database/'.join([dir_name, 'cycleapp.png'])


def insert_image():
    try:
        # Configure connection object
        sqliteConnection = sqlite3.connect(sqlite)
        cursor = sqliteConnection.cursor()
        # save the image in the databases
        sqlite_insert_blob_query = '''INSERT INTO logotype (image) VALUES (?);'''
        with open(img, "rb") as f:
                image = f.read()
        cursor.execute(sqlite_insert_blob_query, (image,))
        # Handle connection close
        sqliteConnection.commit()
        sqliteConnection.close()
        print("Database created")
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

def db_exists():
    try:
        logging.info("Researching Database")
        dburi = 'file:{}?mode=rw'.format(pathname2url(sqlite))
        conn = sqlite3.connect(dburi, uri=True, check_same_thread=False)
        logging.info("Database really exist")
        print("Database really exist")
        conn.close()
    except sqlite3.OperationalError:
        logging.info('Database no exist')
        logging.info('Creating Database')
        open(sqlite, "w")
        try:
            # Configure connection object
            conn = sqlite3.connect(sqlite)
            cur = conn.cursor()
            # Init the setup of database
            initial_script = open(db_script_hard_reset, 'r').read()
            cur.executescript(initial_script)
            # Handle connection close
            conn.commit()
            logging.info("Database Created")
            print("Image inserted successfully as a BLOB into a table")
        except sqlite3.Error:
            logging.exception("Error creating the initial setup")
        finally:
            conn.close()
            insert_image()

db_exists()