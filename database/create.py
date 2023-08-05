import mysql.connector
from mysql.connector import errorcode
import sqlite3

def create_database(cursor,DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("failed ceating database: {}".format(err))
        exit(1)

def createDB(db_NAME):
    DB_NAME = db_NAME
    # cnx = sqlite3.connect(DB_NAME)
    cnx = mysql.connector.connect(host='localhost',port=3306,user='test0')
    cursor= cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} doesn't exits.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor,DB_NAME)
            print("Database created sucessfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    
    return cursor