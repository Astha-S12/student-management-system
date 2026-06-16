import os
import pymysql

def get_db_connection():
    return pymysql.connect(
        host="thomas.proxy.rlwy.net",
        port=58444,
        user="root",
        password=os.getenv("DnLawNxZzqsGzPXWSWHLksNGkUtIkqFG"),
        database="railway",
        cursorclass=pymysql.cursors.DictCursor
    )