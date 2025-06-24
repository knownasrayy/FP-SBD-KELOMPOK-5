# mysql_conn.py
import mysql.connector

def connect_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ecommerce"
    )
