import mysql.connector
from mysql.connector import errorcode
import sqlite3

TABLES = {}
TABLES['tbl_joblist'] =   (
        "CREATE TABLE IF NOT EXISTS tbl_joblist ("
        "job_link VARCHAR(200) NOT NULL,"
        "job_title VARCHAR(200),"
        "company_name VARCHAR(200),"
        "job_type VARCHAR(200),"
        "location VARCHAR(200),"
        "job_description TEXT,"
        "posted_by_name VARCHAR(200),"
        "posted_by_designation VARCHAR(200),"
        "posted_time VARCHAR(20),"
        "is_relevant BOOLEAN,"
        "easy_apply BOOLEAN"
        ")"
    )



DB_NAME = 'job_applydb'

# cnx = sqlite3.connect(DB_NAME)
cnx = mysql.connector.connect(host='localhost',port=3306,user='test0')
cursor = cnx.cursor()

def createSchema():
    for table_name in TABLES:
        desc = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name),end='')
            cursor.execute(desc)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        
    cursor.close()

        